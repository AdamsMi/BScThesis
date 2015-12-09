__author__ = 'Michal'

import os
import numpy
import sys
import math
import cPickle as pickle
import scipy
import time
import scipy.sparse.linalg
import networkx as nx

from file_cleaner import cleaningOfWord
from search_config import  DIR_MATRIX, NUMBER_OF_ARTICLES, DIR_FILES, NGRAM_SIZE
from efficiencydefs import globalefficiency
from collections import defaultdict

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
    for ind, word in enumerate(listOfWords):
        amountOfDocumentsWithGivenTerm = dictOfTermOccurrences[word]
        idf = math.log(float(numberOfArticles)/float(amountOfDocumentsWithGivenTerm), 10)
        matrix[ind,:]*=idf
        idfs.append(idf)
    return matrix, idfs


def gatherAllNGramsFromArticles(listOfArticles, pathToArticles):

    articleInvarints = []
    articlesProcessed = 0

    for currentFileName in listOfArticles:
        articlesProcessed+=1
        if articlesProcessed%100 == 0:
            print "Ngrams gathered from: ", articlesProcessed


        ngram_index = 0
        ngramsDictionary = dict()

        with open(pathToArticles + currentFileName) as currentFile:

            content = currentFile.read()
            ngramGraph = nx.DiGraph()

            contentCleared = ""
            for word in content.split():
                cleanedWord = cleaningOfWord(word)
                if cleanedWord is not None:
                    contentCleared+=cleanedWord + " "

            text = contentCleared.split(" ")
            lastNode = None
            for k in range (0, len(text)-NGRAM_SIZE+1):
                window = ""
                start = k
                end = k + NGRAM_SIZE
                for i in range (start, end):
                    if window=="":
                        window = text[i]
                    else:
                        window = window + " " + text[i]

                node = None
                if ngramsDictionary.has_key(window):
                    node = ngramsDictionary[window]
                else:
                    node = ngram_index
                    ngramsDictionary[window] = ngram_index
                    ngram_index += 1

                if lastNode:
                    ngramGraph.add_edge(lastNode, node)

                lastNode = node


            undirectedGraph = nx.Graph(ngramGraph)

            efficiency = False

            if efficiency:
                articleInvarints.append((
                    ngramGraph.number_of_nodes(),
                    ngramGraph.number_of_edges(),
                    nx.number_strongly_connected_components(ngramGraph),
                    nx.average_clustering(undirectedGraph),
                    globalefficiency(undirectedGraph)
                ))
            else:
                articleInvarints.append((
                    ngramGraph.number_of_nodes(),
                    ngramGraph.number_of_edges(),
                    nx.number_strongly_connected_components(ngramGraph),
                    nx.average_clustering(undirectedGraph)
                ))


    return articleInvarints


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
            for word in currentFile.read().split():
                    if word in words:
                        indexesOfWordsInCurrentFile.append(dictOfWords[word])
                    else:
                        dictOfTermOccurrences[word] = 1
                        words.add(word)
                        dictOfWords[word] = wordAmount
                        mapOfWords.append(word)
                        indexesOfWordsInCurrentFile.append(wordAmount)
                        wordAmount+=1

            workingListOfOccurrences.append(indexesOfWordsInCurrentFile)


    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x, obj in enumerate(workingListOfOccurrences):
        for index in obj:
            matrix[index,x]+=1
        for index in set(obj):
            dictOfTermOccurrences[mapOfWords[index]]+=1


    return words, dictOfWords, matrix, dictOfTermOccurrences, mapOfWords

def writeDataToFile(matrix, dictOfThingsToDump):
    """

    :param matrix: the main matrix
    :param dictOfThingsToDump: mapping (nameOfFileToWrite) -> (content)
    """

    mat = scipy.sparse.csc_matrix(matrix)

    with open(DIR_MATRIX + 'data.pkl', 'wb') as output:
        pickle.dump(mat.data, output)

    with open(DIR_MATRIX + 'indices.pkl', 'wb') as output:
        pickle.dump(mat.indices, output)

    with open(DIR_MATRIX + 'indptr.pkl', 'wb') as output:
        pickle.dump(mat.indptr, output)

    for x in dictOfThingsToDump.keys():
        with open(DIR_MATRIX + x + '.pkl', 'wb') as output:
            pickle.dump(dictOfThingsToDump[x], output)


if __name__ == '__main__':

    only_ngrams = True

    print "Imports done"

    listOfArticleFiles = filter(lambda x: x[0] != '.',sorted(os.listdir(DIR_FILES)))
    amountOfFiles = len(listOfArticleFiles)

    print "Amount of files: ", amountOfFiles
    print

    if(amountOfFiles<1):
        sys.exit("Wrong content of directory to be processed")

    start = time.time()
    articleInvarints = gatherAllNGramsFromArticles(listOfArticleFiles, DIR_FILES)
    stop = time.time()

    print "Gathering n-grams done, took: ", stop-start, " seconds"

    if only_ngrams:
        start = time.time()
        with open(DIR_MATRIX + "articleInvariants" + '.pkl', 'wb') as output:
            pickle.dump(articleInvarints, output)
        stop = time.time()
        print "Writing to file done, took: ", stop - start, " seconds\n"
        exit()

    print "Gathering n-grams done, took: ", stop-start, " seconds"

    start = time.time()
    setOfWords , mapOfWords, matrix, dictOfTermOccurrences, listOfWords= gatherAllWordsFromArticles(listOfArticleFiles, DIR_FILES)
    stop = time.time()

    print "Gathering words done, took: ", stop-start, " seconds"
    print "Amount of words: ", len(setOfWords), "\n"

    start = time.time()
    matrix, idfs = idf(matrix, amountOfFiles,dictOfTermOccurrences, listOfWords)
    stop = time.time()

    print "IDF done, took : ", stop-start, " seconds\n"

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

                              "idfs" : idfs,
                              "articleInvariants": articleInvarints
                            })
    stop = time.time()

    print "Writing to file done, took: ", stop - start, " seconds\n"



