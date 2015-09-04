__author__ = 'Michal'

import os
import numpy
import sys
import math
import cPickle as pickle
import scipy
import time
import scipy.sparse.linalg

RANK_OF_APPROXIMATION =400
NUMBER_OF_ARTICLES = 6000

DIR = 'fil/files/'

def normalization(matrix, amountOfDocuments):
    """
    Function applying normalization to the main matrix
    :param matrix: s.e.
    :param amountOfDocuments:s.e.
    :return: modified matrix
    """

    matrixSparse = scipy.sparse.csc_matrix(matrix)

    nonzeroIndices = matrixSparse.nonzero()
    firstList = nonzeroIndices[0]
    secondList = nonzeroIndices[1]
    amountOfNonZeroCells = len(firstList)
    sumList = [0 for x in xrange(amountOfDocuments)]

    for cellIndex in xrange(amountOfNonZeroCells):
        sumList[secondList[cellIndex]]+=matrix[firstList[cellIndex], secondList[cellIndex]]**2

    for x in xrange(len(sumList)):
        sumList[x] = math.sqrt(sumList[x])

    for cellInd in xrange(amountOfNonZeroCells):
        matrix[firstList[cellInd], secondList[cellInd]]/=sumList[secondList[cellInd]]


    return matrix

def idf(matrix, numberOfArticles, dictOfTermOccurrences, listOfWords):
    """
    Function applying idf to the main matrix.
    :param matrix: the main matrix
    :param numberOfArticles: s.e.
    :param dictOfTermOccurrences: mapping (term) -> (amounfOfDocsWithTerm)
    :param listOfWords: all words
    :return: modified matrix, list of idf values
    """

    idfs = []
    for x in xrange(len(listOfWords)):
        amountOfDocumentsWithGivenTerm = dictOfTermOccurrences[listOfWords[x]]
        idf = math.log(float(numberOfArticles)/float(amountOfDocumentsWithGivenTerm), 10)
        matrix[x,:]*=idf
        idfs.append(idf)
    return matrix, idfs


def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    """
    Gather all words from a given list of articles.
    Opened files format: [pathToArticles + x for x in listOfArticles]

    :param listOfArticles: list of article names
    :param pathToArticles: directory with articles
    :return:    words - set of all words,
                dictOfWords - mapping (word) -> (word's id)
                matrix - bag of words
                dictOfTermOccurrences -
    """

    wordAmount = 0
    words = set()
    dictOfWords = dict()
    dictOfTermOccurrences = dict()

    workingListOfOccurrences = []
    mapOfWords = []

    for currentFileName in listOfArticles:
        with open(pathToArticles + currentFileName) as currentFile:
            indexesOfWordsInCurrentFile = []
            for line in currentFile:
                for word in line.split():
                        if word in words:
                            indexesOfWordsInCurrentFile.append(dictOfWords[word])

                        else:
                            dictOfTermOccurrences[word] = 0
                            words.add(word)
                            dictOfWords[word] = wordAmount
                            mapOfWords.append(word)
                            indexesOfWordsInCurrentFile.append(wordAmount)
                            wordAmount+=1

            workingListOfOccurrences.append(indexesOfWordsInCurrentFile)


    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x in xrange(len(workingListOfOccurrences)):
        for index in workingListOfOccurrences[x]:
            matrix[index,x]+=1
            dictOfTermOccurrences[mapOfWords[x]]+=1


    return words, dictOfWords, matrix, dictOfTermOccurrences, mapOfWords

def writeDataToFile(matrix, dictOfThingsToDump):
    """

    :param matrix: the main matrix
    :param dictOfThingsToDump: mapping (nameOfFileToWrite) -> (content)
    """

    mat = scipy.sparse.csc_matrix(matrix)

    with open('dumps/data.pkl', 'wb') as output:
        pickle.dump(mat.data, output)

    with open('dumps/indices.pkl', 'wb') as output:
        pickle.dump(mat.indices, output)

    with open('dumps/indptr.pkl', 'wb') as output:
        pickle.dump(mat.indptr, output)

    for x in dictOfThingsToDump.keys():
        with open('dumps/' + x + '.pkl', 'wb') as output:
            pickle.dump(dictOfThingsToDump[x], output)


if __name__ == '__main__':

    print "Imports done"

    listOfArticleFiles = filter(lambda x: x[0] != '.',sorted(os.listdir(DIR)))[:NUMBER_OF_ARTICLES]


    amountOfFiles = len(listOfArticleFiles)

    print "Amount of files: ", amountOfFiles


    if(amountOfFiles<1):
        sys.exit("Wrong content of directory to be processed")

    start = time.time()
    setOfWords , mapOfWords, matrix, dictOfTermOccurrences, listOfWords= gatherAllWordsFromArticles(listOfArticleFiles, DIR)
    stop = time.time()

    print "Gathering words done, took: ", stop-start, " seconds\n"
    print "Amount of words: ", len(setOfWords), "\n"

    start = time.time()
    matrix, idfs = idf(matrix, amountOfFiles,dictOfTermOccurrences, listOfWords)
    stop = time.time()

    print "idf done, took : ", stop-start, " seconds\n"

    start = time.time()
    matrix = normalization(matrix, amountOfFiles)
    stop = time.time()

    print "Normalization done, took: ", stop-start, " seconds\n"

    start = time.time()
    writeDataToFile(matrix, { "amountOfWords" : len(setOfWords),
                              "mapOfWords" : mapOfWords,
                              "amountOfFiles" :  amountOfFiles,
                              "dictOfTermOccurrences" : dictOfTermOccurrences,
                              "listOfArticleFiles" : listOfArticleFiles,
                              "idfs" : idfs
                            })
    stop = time.time()

    print "Writing to file done, took: ", stop - start, " seconds\n"



