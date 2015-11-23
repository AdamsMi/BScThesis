__author__ = 'Michal'

import pickle
import time
import webbrowser
import numpy as np

from database_manager   import DatabaseManager
from sparsesvd          import sparsesvd
from search_config      import NGRAM_SIZE
from scipy.sparse       import csc_matrix, lil_matrix
from file_cleaner       import cleaningOfWord
from search_config      import RANK_OF_APPROXIMATION, NUMBER_OF_RESULTS
from search_config      import DIR_MATRIX, DIR_CLUST_CENTROIDS

def sparseLowRankAppr(matrix, rank):
    ut, s, vt = sparsesvd(matrix, rank)
    #print len(ut[0])
    #print len(ut)
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


def createBagOfWordsFromVector(vector, amountOfTerms, dictionary, idfs):
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

    def __init__(self):

        # Load all data
        self.matrix, self.amountOfWords, self.dictOfWords, \
        self.amountOfFiles, self.listOfArticles, self.idfs, \
        self.articleInvariants = loadData(DIR_MATRIX)
        self.matrix = sparseLowRankAppr(self.matrix, RANK_OF_APPROXIMATION)

        print "Data loaded from files & Matrix built\n"
        print 'matrix shape: ', self.matrix.shape
    def search(self, text):

        # Gather correlations
        vector = text.split()
        cleanedVector = cleanVector(vector)
        bagOfWords, indices = createBagOfWordsFromVector(cleanedVector, self.amountOfWords, self.dictOfWords, self.idfs)

        b = fasterCorrelations(self.matrix, indices, bagOfWords, self.amountOfFiles)

        print 'correlations'
        print b
        # Get links from database
        dbMan = DatabaseManager()
        results = []
        for x in b:
            #print x
            #print self.listOfArticles[x[0]]
            results.append(dbMan.get_link(self.listOfArticles[x[0]]))

        # Return response dictionary
        return results


if __name__ == '__main__':
    searchClient = SearchClient()
    dm = DatabaseManager()

    typeOfSearch = 2#int(raw_input('(1) Query-search or (2) drill-down:'))

    if typeOfSearch ==1:

        while (True):
            results  = searchClient.search(raw_input("Input"))
            print results
    else:
        from k_means import get_document_clustering
        clus = get_document_clustering(np.transpose(searchClient.matrix))

        with open(DIR_CLUST_CENTROIDS + 'closestArt', 'rb') as input:
            centerArticles = pickle.load(input)

        with open(DIR_CLUST_CENTROIDS + 'res_limited', 'rb') as input:
            categoriesClusters = pickle.load(input)


        for k in clus.keys():
            print '\n\n Cluster nr: ', k
            for cat in categoriesClusters[str(k)]:
                print cat[0]
            print centerArticles[k]
            print 'amount of articles in the cluster: ', len(clus[k])

        print '\n'
        chosenCluster = int(raw_input('Choose cluster nr:'))
        print '\n'
        articlesAmountInCurrentClust = len(clus[chosenCluster])

        if len(clus[chosenCluster]) <=10:
            ct = 1
            articleNumbers = clus[chosenCluster]
            for artNo in articleNumbers:
                title = searchClient.listOfArticles[artNo]
                ans = dm.get_link(title).title
                print ct, ': ', ans
                ct+=1
            choice = int(raw_input('Nr of the chosen article: '))

            title = searchClient.listOfArticles[articleNumbers[choice-1]]
            ans = dm.get_link(title).url
            webbrowser.open(ans)

        else:
            while articlesAmountInCurrentClust>10:
                indices = sorted(clus[chosenCluster])

                submatrix = searchClient.matrix[:, indices]
                howManyClusters = 12 if articlesAmountInCurrentClust>20 else 6

                clus = get_document_clustering(np.transpose(submatrix), initial=False, nrOfClusters= howManyClusters)
                print clus
                for k in clus.keys():
                    indxs = [indices[l] for l in clus[k]]
                    print '\n\nCluster nr:', k
                    centroid = calcCentroid(searchClient.matrix, indxs)
                    closest= findArticleClosestToCentroid(indxs, centroid, searchClient.matrix)
                    title = searchClient.listOfArticles[closest[0]]
                    newTitle = dm.get_link(title).title
                    print newTitle
                    print 'amount of articles in the cluster: ', len(indxs)
                chosenCluster = int(raw_input('\n\nChoose cluster nr:'))
                articlesAmountInCurrentClust = len(clus[chosenCluster])
            ct = 1
            articleNumbers = sorted(clus[chosenCluster])
            ndxs = [indices[l] for l in articleNumbers]
            for artNo in ndxs:
                title = searchClient.listOfArticles[artNo]
                ans = dm.get_link(title).title
                print ct, ': ', ans
                ct+=1
            choice = int(raw_input('Nr of the chosen article: '))

            title = searchClient.listOfArticles[ndxs[choice-1]]
            ans = dm.get_link(title).url
            webbrowser.open(ans)