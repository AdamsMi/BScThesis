__author__ = 'Michal'

import os
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import numpy
import sys
import math

directoryOfDataset = 'files/'
stemmer = SnowballStemmer('english')


def inverseDocumentFrequency(matrix, mapOfWords, numberOfDocuments):
    for x in xrange(len(mapOfWords)):
        amountOfDocumentsWithGivenTerm = 0
        for y in xrange(numberOfDocuments):
            amountOfDocumentsWithGivenTerm+= 1 if matrix[x,y] > 0 else 0
        #print str(x) + " " + str(amountOfDocumentsWithGivenTerm) + "\n"
        idf = math.log(float(numberOfDocuments)/float(amountOfDocumentsWithGivenTerm),10)
        print idf
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
    return word

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):

    words = set()
    mapOfWords = []
    workingListOfOccurences = []

    for currentFileName in listOfArticles:
        currentFile = open(pathToArticles + currentFileName)
        indexesOfWordsInCurrentFile = []
        for line in currentFile:
            for word in line.split():
                cleanedWord = cleaningOfWord(word)
                if not cleanedWord is None:

                    if cleanedWord in words:
                        indexesOfWordsInCurrentFile.append(mapOfWords.index(cleanedWord))

                    else:
                        words.add(cleanedWord)
                        mapOfWords.append(cleanedWord)

                        indexesOfWordsInCurrentFile.append(len(words)-1)

        workingListOfOccurences.append(indexesOfWordsInCurrentFile)
        currentFile.close()

    matrix = numpy.zeros((len(words), len(listOfArticles)), float)

    for x in xrange(len(workingListOfOccurences)):
        for index in workingListOfOccurences[x]:
            matrix[index,x]+=1

    return words, mapOfWords, matrix

if __name__ == '__main__':

    print "Imports done"

    listOfArticleFiles =   sorted(os.listdir(directoryOfDataset))

    print "list of articles created :\n"

    print listOfArticleFiles

    if(len(listOfArticleFiles)<1):
        sys.exit("Wrong content of directory to be processed")


    setOfWords , mapOfWords, matrix= gatherAllWordsFromArticles(listOfArticleFiles, directoryOfDataset)


    matrix = inverseDocumentFrequency(matrix, mapOfWords, len(listOfArticleFiles))

    print "Matrix"
    print matrix

    print "map of words"
    print mapOfWords
