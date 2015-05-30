__author__ = 'Michal'

import os
import numpy
import sys
import math
from scipy import linalg
import pickle
import scipy
import time
import scipy.sparse.linalg
from sparsesvd import sparsesvd

RANK_OF_APPROXIMATION =100

directoryOfDataset = 'files/'

def low_rank_approx( matrix, rank):

    start = time.time()
    U, d, Vt = linalg.svd(matrix)
    stop = time.time()
    print "linalg.svd took: ", stop - start, " seconds\n"

    start = time.time()
    D = linalg.diagsvd(d, matrix.shape[0], matrix.shape[1])
    stop = time.time()
    print "linalg.diagsvd took: ", stop - start, " seconds\n"

    start = time.time()
    D1 = D.copy()
    stop = time.time()
    print "D.copy took: ", stop - start, " seconds\n"

    start = time.time()
    D1[D1 < d[int(rank)]] = 0.
    stop = time.time()
    print "Reseting small singular values took: ", stop-start, " seconds\n"
    return  numpy.dot(numpy.dot(U, D1), Vt)

def sparseLowRankAppr(matrix, rank):
    smat = scipy.sparse.csc_matrix(matrix)
    ut, s, vt = sparsesvd(smat, rank)
    return numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt))


def normalization(matrix, amountOfDocuments):
    matrixSparse = scipy.sparse.csc_matrix(matrix)

    nonzeroIndices = matrixSparse.nonzero()
    firstList = nonzeroIndices[0]
    secondList = nonzeroIndices[1]
    amountOfNonZeroCells = len(firstList)
    sumList = [0 for x in xrange(amountOfDocuments)]

    for cellIndex in xrange(amountOfNonZeroCells):
        sumList[secondList[cellIndex]]+=matrix[firstList[cellIndex], secondList[cellIndex]]**2

    for cellInd in xrange(amountOfNonZeroCells):
        matrix[firstList[cellInd], secondList[cellInd]]/=sumList[secondList[cellInd]]

    return matrix


def idf(matrix, numberOfWords, numberOfArticles, dictOfTermOccurences, listOfWords):
    for x in xrange(numberOfWords):
        amountOfDocumentsWithGivenTerm = dictOfTermOccurences[listOfWords[x]]
        idf = math.log(float(numberOfArticles)/float(amountOfDocumentsWithGivenTerm), 10)
        matrix[x,:]*=idf
    return matrix

def createDictionaryForWordIndexes(wordsSet):
    dictionaryInProgress = dict()
    for x in xrange(len(wordsSet)):
        dictionaryInProgress[wordsSet[x]] = x

    return dictionaryInProgress

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    wordAmount = 0
    words = set()
    dictOfWords = dict()
    dictOfTermOccurences = dict()

    workingListOfOccurences = []
    mapOfWords = []

    for currentFileName in listOfArticles:
        currentFile = open(pathToArticles + currentFileName)
        indexesOfWordsInCurrentFile = []
        for line in currentFile:
            for word in line.split():
                    if word in words:
                        indexesOfWordsInCurrentFile.append(dictOfWords[word])

                    else:
                        dictOfTermOccurences[word] = 0
                        words.add(word)
                        dictOfWords[word] = wordAmount
                        mapOfWords.append(word)
                        indexesOfWordsInCurrentFile.append(wordAmount)
                        wordAmount+=1

        workingListOfOccurences.append(indexesOfWordsInCurrentFile)
        currentFile.close()

    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x in xrange(len(workingListOfOccurences)):
        for index in workingListOfOccurences[x]:
            matrix[index,x]+=1
        wordsInDocument = set(workingListOfOccurences[x])
        for x in wordsInDocument:
            dictOfTermOccurences[mapOfWords[x]]+=1


    return words, dictOfWords, matrix, dictOfTermOccurences, mapOfWords

def writeDataToFile(matrix, setOfWords, mapOfWords, amountOfFiles):

    mat = scipy.sparse.csc_matrix(matrix)

    start= time.time()

    with open('dumps/data.pkl', 'wb') as output:
        pickle.dump(mat.data, output)

    with open('dumps/indices.pkl', 'wb') as output:
        pickle.dump(mat.indices, output)

    with open('dumps/indptr.pkl', 'wb') as output:
        pickle.dump(mat.indptr, output)

    stop = time.time()
    print "Writing matrix to file took: ", stop-start, "seconds \n"

    start = time.time()
    output = open('dumps/words.pkl', 'wb')
    pickle.dump(setOfWords, output)
    output.close()
    stop = time.time()
    print "Writing set of words to file took: ", stop-start, "seconds \n"

    start = time.time()
    output = open('dumps/wordsMap.pkl', 'wb')
    pickle.dump(mapOfWords, output)
    output.close()

    output = open('dumps/documentsAmount.pkl', 'wb')
    pickle.dump(amountOfFiles, output)
    output.close()
    stop = time.time()
    print "Writing map and amount of files to files took: ", stop-start, "seconds \n"

if __name__ == '__main__':

    print "Imports done"

    listOfArticleFiles =   sorted(os.listdir(directoryOfDataset))[:500]

    amountOfFiles = len(listOfArticleFiles)

    print "Amount of files: ", amountOfFiles


    if(amountOfFiles<1):
        sys.exit("Wrong content of directory to be processed")

    start = time.time()
    setOfWords , mapOfWords, matrix, dictOfTermOccurences, listOfWords= gatherAllWordsFromArticles(listOfArticleFiles, directoryOfDataset)
    stop = time.time()

    print "Gathering words done, took: ", stop-start, " seconds\n"
    print "Amount of words: ", len(setOfWords), "\n"

    start = time.time()
    matrix = idf(matrix, len(setOfWords), amountOfFiles,dictOfTermOccurences, listOfWords)
    stop = time.time()

    print "idf done, took : ", stop-start, " seconds\n"



    start = time.time()
    matrix = normalization(matrix, amountOfFiles)
    stop = time.time()

    print "Normalization done, took: ", stop-start, " seconds\n"

    print "Low rank appr done, took: ", stop-start, " seconds\n"

    start = time.time()
    writeDataToFile(matrix, setOfWords, mapOfWords, amountOfFiles)
    stop = time.time()

    print "Writing to file done, took: ", stop - start, " seconds\n"

