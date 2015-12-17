import time
import pickle
import numpy as np
import webbrowser

from database_manager           import DatabaseManager
from sparsesvd                  import sparsesvd
from search_config              import NGRAM_SIZE, CLUST_DIR
from scipy.sparse               import csc_matrix, lil_matrix
from file_cleaner               import cleaningOfWord
from search_config              import RANK_OF_APPROXIMATION, NUMBER_OF_RESULTS
from search_config              import DIR_MATRIX, DIR_CLUST_CENTROIDS
from k_means                    import get_document_clustering
from stemming_mapper            import getFreqWordsForClustering
from lda_transformation         import getLDAModel
from k_means_centroid_manager   import calculateCentroidsForClustering


def sparseLowRankAppr(matrix, rank):
    ut, s, vt = sparsesvd(matrix, rank)
    return np.dot(ut.T, np.dot(np.diag(s), vt))

def calcCentroid(matrix, indices):
    startingPoint = matrix[:, indices[0]]
    for ind in indices[1:]:
        startingPoint += matrix[:, ind]
    return startingPoint

def findArticleClosestToCentroid(listOfDocNumbers, centroid, mtx):
    if len(listOfDocNumbers)==1:
        return (listOfDocNumbers[0], 1.0)
    a = []
    sim = 0.0
    for x in listOfDocNumbers:
        for ind in xrange(len(centroid)):
            sim += centroid[ind] * mtx[ind, x]
        a.append((x,sim))
        sim = 0.0
    return sorted(a, key = lambda x: x[1], reverse=True)[0]


def loadData(directory):
    with open(directory + 'data.pkl', 'rb') as inputFile:
        data = pickle.load(inputFile)

    inputFile = open(directory + 'indices.pkl', 'rb')
    indices = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'indptr.pkl', 'rb')
    indptr = pickle.load(inputFile)
    inputFile.close()

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'amountOfFiles.pkl', 'rb') as inputFile:
        amountOfFiles = pickle.load(inputFile)

    with open(directory + 'listOfArticleFiles.pkl', 'rb') as inputFile:
        listOfArticleFiles = pickle.load(inputFile)

    with open(directory + 'articleInvariants.pkl', 'rb') as inputFile:
        ngramsInvariants = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)


    return csc_matrix((data, indices, indptr)), amountOfWords, mapOfWords, \
           amountOfFiles, listOfArticleFiles, idfs, ngramsInvariants


def cleanVector(vector):
    cleanedVector = []
    for word in vector:
        cleanWord = cleaningOfWord(word)
        if cleanWord is not None:
            cleanedVector.append(cleanWord)
    return cleanedVector


def createBagOfWordsFromVector(vector, amountOfTerms, dictionary, idfs=None):
    bagOfWords = lil_matrix((1, amountOfTerms), dtype=float)
    indices = []
    for x in vector:
        try:
            ind = dictionary[x]
            bagOfWords[0, ind] += 1
            bagOfWords[0, ind] *= idfs[ind]
            indices.append(ind)
        except:
            continue
    bagOfWords = csc_matrix(bagOfWords, dtype=float)
    return bagOfWords, indices



def createBagOfWordsForLDA(vector, amountOfTerms, dictionary):
    bow = np.zeros((1, amountOfTerms), float)
    for word in vector:
        try:
            ind = dictionary[word]
            bow[0, ind] += 1
        except:
            continue
    print bow.shape
    return bow

def createNgramsVectorForWord(vector, ngramsDictionary):
    nGramsVector = []

    for k in range (0, len(vector)-NGRAM_SIZE+1):
        window = ""
        start = k
        end = k + NGRAM_SIZE
        for i in range (start, end):
            if window=="":
                window = vector[i]
            else:
                window = window + " " + vector[i]

        if ngramsDictionary.has_key(window):
                nGramsVector.append(ngramsDictionary[window])

    return nGramsVector

def nGramsCorrelations(titleNgrams, articleNgrams):
    similarities = []
    for x in xrange(len(articleNgrams)):
        result = set(articleNgrams[x]).intersection(titleNgrams)
        maxNgrams = float(max(len(articleNgrams[x]), len(titleNgrams)))
        similarities.append((x, len(result)/maxNgrams))

    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:5]


def findCorrelations(matrix, vector, amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = vector.dot(matrix[:, x])[0]
        similarities.append((x, simil))
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:5]


def fasterCorrelations(matrix, indices, vector,  amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = 0
        for ind in indices:
            simil += matrix[ind,x] * vector[0,ind]
        similarities.append((x, simil))
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:NUMBER_OF_RESULTS]

class SearchClient(object):

    def __init__(self, dm, calcSVD = True, calcLDA = True):

        # Load all data
        self.dm = dm
        self.matrix, self.amountOfWords, self.dictOfWords, \
        self.amountOfFiles, self.listOfArticles, self.idfs, \
        self.articleInvariants = loadData(DIR_MATRIX)
        start = time.time()

        # dbMan = DatabaseManager()
        # for ind, el in enumerate(self.listOfArticles):
        #     title = dbMan.get_link(el).title
        #     if 'Webchat' in title:
        #         print title
        #         print el

        if calcSVD:
            self.matrix = sparseLowRankAppr(self.matrix, RANK_OF_APPROXIMATION)

            print "Data loaded from files & Matrix built\n"
            print 'SVD took: ', time.time() - start
            print 'matrix shape: ', self.matrix.shape

        if calcLDA:
            self.model, self.wordsToAsk = getLDAModel()

            start = time.time()
            print 'LDA model built'
            print 'Fitting LDA model took: ', time.time() - start

            #print 'topic word shape', self.model.topic_word_.shape
            #print 'doc topic shape', self.model.doc_topic_.shape


    def search(self, text, isSvd = False):
        start = time.time()
        vector = text.split()
        cleanedVector = cleanVector(vector)
        #cleanedVector = self.wordsToAsk

        print cleanedVector

        if isSvd:
            bagOfWords, indices = createBagOfWordsFromVector(cleanedVector, self.amountOfWords, self.dictOfWords, self.idfs)
            b = fasterCorrelations(self.matrix, indices, bagOfWords, self.amountOfFiles)

        else:
            bagOfWords = createBagOfWordsForLDA(cleanedVector, self.amountOfWords, self.dictOfWords)

            #print 'bow shape:'
            #print bagOfWords.shape

            #print 'topic word shape:'
            #print np.transpose(self.model.topic_word_).shape
            res = np.dot(bagOfWords, np.transpose(self.model.topic_word_))

            #print 'first mul shape:'
            #print res.shape
            #print res
            #print 'doc topic shape:'
            #print np.transpose(self.model.doc_topic_).shape

            res2 = np.dot(res, np.transpose(self.model.doc_topic_))

            #print 'final shape:'
            #print res2.shape

            bestValues = sorted(list(res2[0]), reverse=True)[:5]

            b = []

            for bestVal in bestValues:
                for ind, val in enumerate(list(res2[0])):
                    if val == bestVal:
                        b.append((ind, val))


        results = []
        dbMan = DatabaseManager()
        for x in b:
            results.append(dbMan.get_link(self.listOfArticles[x[0]]))

        for res in results:
            print res.url
            print res.title

        stop = time.time()
        return results, stop - start


    def getInitialClustering(self):

        clustering = get_document_clustering(np.transpose(self.matrix), fileName='')
        calculateCentroidsForClustering(clustering, clusteringName = '',
                                        mat = self.matrix, ngramsMat=self.articleInvariants)
        freqWords = getFreqWordsForClustering(clustering, self.dictOfWords, '', self, self.dm)

        with open(DIR_CLUST_CENTROIDS + 'res_limited', 'rb') as input:
            categoriesClusters = pickle.load(input)
        res = dict()
        for k in categoriesClusters.keys():
            res[int(k)] = [a[0] for a in categoriesClusters[k]]

        return clustering, res, freqWords


    def getClustering(self, drillDownPath):


        fileName = ''
        formerFileName = ''
        for ind in drillDownPath:
            formerFileName = fileName
            fileName+='_' + str(ind)


        with open(CLUST_DIR + 'b' + formerFileName + '.pickle',  'rb') as handle:
            formerClust = pickle.load(handle)

        artNumbers = formerClust[drillDownPath[-1]]

        if len(artNumbers) <= 10:
            return [], []

        amountOfClusters = 12 if len(artNumbers)>30 else 6
        clustering = get_document_clustering(np.transpose(self.matrix[:,artNumbers]),
                                             fileName = fileName,
                                             actualIndexes = artNumbers,
                                             nrOfClusters = amountOfClusters)
        calculateCentroidsForClustering(clustering,
                                        clusteringName = fileName,
                                        mat = self.matrix,
                                        ngramsMat=self.articleInvariants)
        freqWords =getFreqWordsForClustering(clustering, self.dictOfWords, fileName, self, self.dm)

        return clustering, freqWords


    def getArticles(self, drillDownPath):

        fileName = ''
        formerFileName = ''
        for ind in drillDownPath:
            formerFileName = fileName
            fileName+='_' + str(ind)

        with open(CLUST_DIR + 'b' + formerFileName + '.pickle',  'rb') as handle:
            formerClust = pickle.load(handle)

        artNumbers = formerClust[drillDownPath[-1]]

        results = []
        dbMan = DatabaseManager()
        for x in artNumbers:
            results.append(dbMan.get_link(self.listOfArticles[x]))

        return results



if __name__ == '__main__':
    dm = DatabaseManager()
    searchClient = SearchClient(dm)
    #clust, labels, words = searchClient.getInitialClustering()
    #print words
    #clust, words = searchClient.getClustering([0])
    #print clust
    #print words

    #searchClient.search('David cameron uk immigrants')


    a= 1
    while (a>0):
        results, timeOfQuery = searchClient.search('David cameron uk immigrants', isSvd=True)

        print "Search completed in ", timeOfQuery

        results, timeOfQuery = searchClient.search('David cameron uk immigrants')

        print "Search completed in ", timeOfQuery
        a-=1
