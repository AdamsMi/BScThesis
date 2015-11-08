__author__ = 'Michal'

import pickle
import time
import numpy
import webbrowser
import numpy as np

from database_manager   import DatabaseManager
from sparsesvd          import sparsesvd
from search_config      import NGRAM_SIZE
from scipy.sparse       import csc_matrix, lil_matrix
from file_cleaner       import cleaningOfWord
from search_config      import RANK_OF_APPROXIMATION, NUMBER_OF_RESULTS
from search_config      import DIR_MATRIX

def sparseLowRankAppr(matrix, rank):
    ut, s, vt = sparsesvd(matrix, rank)
    print len(ut[0])
    print len(ut)
    return numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt))


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

    with open(directory + 'ngramsDict.pkl', 'rb') as inputFile:
        ngramsDict = pickle.load(inputFile)

    with open(directory + 'articlesNgrams.pkl', 'rb') as inputFile:
        articlesNgrams = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)


    return csc_matrix((data, indices, indptr)), amountOfWords, mapOfWords, \
           amountOfFiles, listOfArticleFiles, idfs, articlesNgrams, ngramsDict


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
            print "one of the words not in out dataset, that is to say: %s" % x
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
        self.articleTitleNgrams, self.nGramsDict = loadData(DIR_MATRIX)

        self.matrix = sparseLowRankAppr(self.matrix, RANK_OF_APPROXIMATION)
        print "Data loaded from files & Matrix built\n"

    def search(self, text):
        start = time.time()

        # Gather correlations
        vector = text.split()
        cleanedVector = cleanVector(vector)
        bagOfWords, indices = createBagOfWordsFromVector(cleanedVector, self.amountOfWords, self.dictOfWords, self.idfs)

        corellationNgrams = []
        if (len(cleanedVector)>=NGRAM_SIZE):
            nGramsVector = createNgramsVectorForWord(cleanedVector, self.nGramsDict)
            corellationNgrams = nGramsCorrelations(nGramsVector, self.articleTitleNgrams)


        b = fasterCorrelations(self.matrix, indices, bagOfWords, self.amountOfFiles)

        print 'correlations'
        print b
        # Get links from database
        dbMan = DatabaseManager()
        results = []
        for x in b:
            print x
            print self.listOfArticles[x[0]]
            results.append(dbMan.get_link(self.listOfArticles[x[0]]))
        stop = time.time()

        # Return response dictionary
        return results, stop-start


if __name__ == '__main__':
    searchClient = SearchClient()


    print 'starting clustering\n'
    from k_means import get_document_clustering
    clus = get_document_clustering(np.transpose(searchClient.matrix))
    import pprint as pp
    #pp.pprint(clus)
    #for x in clus.keys():
    #    print x, len(clus[x])
    #print 'done clustering\n'

    while (True):
        #results, timeOfQuery = searchClient.search(raw_input("Input: "))
        artNr = int(raw_input('article nr'))
        if artNr == -1:
            break
        article = searchClient.listOfArticles[artNr]
        print article
        #for news in results:
        dbMan = DatabaseManager()
        webbrowser.open(dbMan.get_link(article).url)



