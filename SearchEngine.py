__author__ = 'Michal'

import pickle
import scipy

from PreprocessingManager import cleaningOfWord
from PreprocessingManager import inverseDocumentFrequency

def loadData(directory):

    inputFile = open(directory + 'data.pkl', 'rb')
    data = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'indices.pkl', 'rb')
    indices = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'indptr.pkl', 'rb')
    indptr = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'words.pkl', 'rb')
    setOfWords = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'wordsMap.pkl', 'rb')
    mapOfWords = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'documentsAmount.pkl', 'rb')
    amountOfFiles = pickle.load(inputFile)
    inputFile.close()

    return data, indices, indptr, setOfWords, mapOfWords, amountOfFiles

def cleanVector(vector):
    cleanedVector = []
    for word in vector:
        cleanWord = cleaningOfWord(word)
        if cleanWord is not None:
            cleanedVector.append(cleanWord)
    return cleanedVector



def findCorrelations(matrix, vector, amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = bagOfWords.dot(matrix[:, x])[0, 0]
        similarities.append((x, simil))
    return similarities

def createBagOfWordsFromVector(vector, amountOfTerms, dictionary):
    bagOfWords = scipy.sparse.lil_matrix((1, amountOfTerms), dtype=float)
    for x in vector:
        try:
            bagOfWords[0,dictionary[x]]+=1
        except:
            print "one of the words not in out dataset"
            continue
    bagOfWords = scipy.sparse.csc_matrix(bagOfWords, dtype=float)
    return bagOfWords

if __name__ == '__main__':
    matrix, indices, indptr, setOfWords, dictOfWords, amountOfFiles= loadData('dumps/')
    matrix = scipy.sparse.csc_matrix((matrix, indices, indptr))
    print "Data loaded from files & Matrix built\n"
    vector = raw_input("Input: ").split()

    cleanedVect =  cleanVector(vector)
    bagOfWords = createBagOfWordsFromVector(cleanedVect, len(setOfWords), dictOfWords)
    print bagOfWords
    print findCorrelations(matrix, bagOfWords, amountOfFiles)

