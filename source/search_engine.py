
__author__ = 'Michal'

import pickle
import time
import numpy
import webbrowser


from source.database_manager import DatabaseManager
from sparsesvd import sparsesvd
from scipy.sparse import csc_matrix, lil_matrix
from source.file_cleaner import cleaningOfWord
from search_config import RANK_OF_APPROXIMATION

from search_config import DIR_DUMPS


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

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return csc_matrix((data, indices, indptr)), amountOfWords, mapOfWords, amountOfFiles, listOfArticleFiles, idfs


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
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:5]

if __name__ == '__main__':
    matrix, amountOfWords, dictOfWords, amountOfFiles, listOfArticles, idfs = loadData(DIR_DUMPS)
    matrix = sparseLowRankAppr(matrix, RANK_OF_APPROXIMATION)
    print "Data loaded from files & Matrix built\n"



    vector = raw_input("Input: ").split()
    cleanedVect = cleanVector(vector)

    bagOfWords, indices = createBagOfWordsFromVector(cleanedVect, amountOfWords, dictOfWords, idfs)
    #tart = time.time()
    #a = findCorrelations(matrix, bagOfWords, amountOfFiles)
    #stop = time.time()
    #print "old correlation measure took: ", stop-start, " seconds\n"

    start = time.time()
    b = fasterCorrelations(matrix, indices, bagOfWords, amountOfFiles)
    stop = time.time()
    print "new correlation measure took: ", stop-start, " seconds\n"

    #print a
    print b
    #print a
    dbMan = DatabaseManager()
    for x in b:

        #print dbMan.get_link(listOfArticles[x[0]])

        webbrowser.open(dbMan.get_link(listOfArticles[x[0]])[0])



