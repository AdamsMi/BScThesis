__author__ = 'Michal'

import pickle
from scipy.sparse import csc_matrix, lil_matrix
import numpy
import time
import os

from FileCleaner import cleaningOfWord

MATRIX_FILENAME = 'data.npz'

def load_sparse_csc(filename):
    loader = numpy.load(filename)
    return csc_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def loadData(directory):
    start = time.time()
    matrix = load_sparse_csc(directory + MATRIX_FILENAME)
    stop = time.time()

    with open(directory + 'words.pkl', 'rb') as inputFile:
        setOfWords = pickle.load(inputFile)


    with open(directory + 'wordsMap.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'documentsAmount.pkl', 'rb') as inputFile:
        amountOfFiles = pickle.load(inputFile)

    return matrix, setOfWords, mapOfWords, amountOfFiles


#Just cleans the words from a user's query
def cleanVector(vector):
    cleanedVector = []
    for word in vector:
        cleanWord = cleaningOfWord(word)
        if cleanWord is not None:
            cleanedVector.append(cleanWord)
    return cleanedVector

def createBagOfWordsFromVector(vector, amountOfTerms, dictionary):
    bagOfWords = lil_matrix((1, amountOfTerms), dtype=float)
    for x in vector:
        try:
            bagOfWords[0,dictionary[x]]+=1
        except:
            print "one of the words not in out dataset, that is to say: %s" %x
            continue
    bagOfWords = csc_matrix(bagOfWords, dtype=float)
    return bagOfWords

def findCorrelations(matrix, vector, amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = vector.dot(matrix[:, x])[0, 0]
        similarities.append((x, simil))
    return sorted(similarities, key = lambda tup: tup[1], reverse=True)[:5]


if __name__ == '__main__':
    matrix, setOfWords, dictOfWords, amountOfFiles = loadData('dumps/')
    print "Data loaded from files & Matrix built\n"
    vector = raw_input("Input: ").split()

    cleanedVect =  cleanVector(vector)
    bagOfWords = createBagOfWordsFromVector(cleanedVect, len(setOfWords), dictOfWords)
    a= findCorrelations(matrix, bagOfWords, amountOfFiles)


    list = sorted(os.listdir('files/'))
    for x in a:
        print list[x[0]]


