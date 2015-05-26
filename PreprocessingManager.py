__author__ = 'Michal'

import os
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
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
stemmer = SnowballStemmer('english')


#low-rank approximation of a given matrix
# args: matrix - matrix to be approximated, rank - rank of approximation

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
    start = time.time()
    smat = scipy.sparse.csc_matrix(matrix)
    stop = time.time()
    print "scipy.sparse.csc_matrix took: ", stop - start, " seconds\n"

    start = time.time()
    ut, s, vt = sparsesvd(smat, rank)
    stop = time.time()
    print "sparsesvd took: ", stop - start, " seconds\n"

    return numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt))

def normalization(matrix, amountOfDocuments):
    for x in xrange(amountOfDocuments):
        norm = 0.0
        for a in matrix[:,x]:
            norm+=float(a)**2
        #print "Norm : ", norm
        matrix[:,x]/=norm
    return matrix


def inverseDocumentFrequency(matrix, mapOfWords, numberOfDocuments):
    for x in xrange(len(mapOfWords)):
        amountOfDocumentsWithGivenTerm = 0
        for y in xrange(numberOfDocuments):
            amountOfDocumentsWithGivenTerm+= 1 if matrix[x,y] > 0 else 0
        #print str(x) + " " + str(amountOfDocumentsWithGivenTerm) + "\n"
        idf = math.log(float(numberOfDocuments)/float(amountOfDocumentsWithGivenTerm),10)
        #print idf
        matrix[x,:]*=idf
    return matrix


def createDictionaryForWordIndexes(wordsSet):
    dictionaryInProgress = dict()
    for x in xrange(len(wordsSet)):
        dictionaryInProgress[wordsSet[x]] = x

    return dictionaryInProgress

def cleaningOfWord(wordBeingCleaned):

    wordBeingCleaned = wordBeingCleaned.lower()
    wordBeingCleaned = re.sub('[^A-Za-z0-9]+', '', wordBeingCleaned)
    if wordBeingCleaned in stopwords.words('english'):
        return None

    word = stemmer.stem(wordBeingCleaned).encode('ascii', 'english')
    return word if word != '' else None

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    wordAmount = 0
    words = set()
    dictOfWords = dict()
    mapOfWords = []
    workingListOfOccurences = []
    count =1
    for currentFileName in listOfArticles:
        if count%100==0:
            print "Files preprocessed :", count
        count+=1
        currentFile = open(pathToArticles + currentFileName)
        indexesOfWordsInCurrentFile = []
        for line in currentFile:
            for word in line.split():
                cleanedWord = cleaningOfWord(word)
                if not cleanedWord is None:

                    if cleanedWord in words:
                        indexesOfWordsInCurrentFile.append(dictOfWords[cleanedWord])

                    else:
                        words.add(cleanedWord)
                        dictOfWords[cleanedWord] = wordAmount
                        mapOfWords.append(cleanedWord)

                        indexesOfWordsInCurrentFile.append(wordAmount)
                        wordAmount+=1

        workingListOfOccurences.append(indexesOfWordsInCurrentFile)
        currentFile.close()

    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x in xrange(len(workingListOfOccurences)):
        for index in workingListOfOccurences[x]:
            matrix[index,x]+=1

    return words, mapOfWords, matrix

def writeDataToFile(matrix, setOfWords, mapOfWords, amountOfFiles):
    matrix = scipy.sparse.csc_matrix(matrix)

    output = open('dumps/data.pkl', 'wb')
    pickle.dump(matrix.data, output)
    output.close()

    output = open('dumps/indices.pkl', 'wb')
    pickle.dump(matrix.indices, output)
    output.close()

    output = open('dumps/indptr.pkl', 'wb')
    pickle.dump(matrix.indptr, output)
    output.close()

    output = open('dumps/words.pkl', 'wb')
    pickle.dump(setOfWords, output)
    output.close()


    wordsDict = {}

    for x in xrange(len(mapOfWords)):
        wordsDict[mapOfWords[x]]=x

    print wordsDict

    output = open('dumps/wordsMap.pkl', 'wb')
    pickle.dump(wordsDict, output)
    output.close()

    output = open('dumps/documentsAmount.pkl', 'wb')
    pickle.dump(amountOfFiles, output)
    output.close()



if __name__ == '__main__':

    print "Imports done"

    listOfArticles =   sorted(os.listdir(directoryOfDataset))


    listOfArticleFiles = listOfArticles[:500]

    amountOfFiles = len(listOfArticleFiles)

    print "Amount of files: ", amountOfFiles


    if(amountOfFiles<1):
        sys.exit("Wrong content of directory to be processed")

    start = time.time()
    setOfWords , mapOfWords, matrix= gatherAllWordsFromArticles(listOfArticleFiles, directoryOfDataset)
    stop = time.time()

    print "Words've been gathered from articles, amount: ", len(setOfWords), " it took: ", stop- start, " seconds\n"
    start = time.time()
    matrix = inverseDocumentFrequency(matrix, mapOfWords, amountOfFiles)
    stop = time.time()

    print "idf done, took : ", stop-start, " seconds\n"

    start = time.time()
    matrix = normalization(matrix, amountOfFiles)
    stop = time.time()

    print "Normalization done, took: ", stop-start, " seconds\n"

    matrix = sparseLowRankAppr(matrix, RANK_OF_APPROXIMATION)


    start = time.time()
    writeDataToFile(matrix, setOfWords, mapOfWords, amountOfFiles)
    stop = time.time()

    print "Writing to file done, took: ", stop - start, " seconds\n"
