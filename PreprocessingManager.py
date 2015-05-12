__author__ = 'Michal'

import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import numpy

directoryOfDataset = 'files/'
stemmer = SnowballStemmer('english')

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

    return stemmer.stem(wordBeingCleaned)

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    words = set()

    for currentFileName in listOfArticles:
        currentFile = open(pathToArticles + currentFileName)
        for line in currentFile:
            for word in line.split():
                cleanedWord = cleaningOfWord(word)
                if not cleanedWord is None:
                    words.add(cleanedWord.encode('ascii', 'ignore'))
        currentFile.close()
    return words

if __name__ == '__main__':

    listOfArticleFiles =   sorted(os.listdir(directoryOfDataset))

    print listOfArticleFiles

    setOfWords = gatherAllWordsFromArticles(listOfArticleFiles, directoryOfDataset)


    Matrix = numpy.zeros((len(setOfWords), len(listOfArticleFiles)), float)


    wordDict = createDictionaryForWordIndexes(sorted(list(setOfWords)))

    print wordDict

    for x in xrange(len(listOfArticleFiles)):
        bagOfWordsForArticle = numpy.zeros(len(setOfWords), float)

        file = open(directoryOfDataset + listOfArticleFiles[x])

        for line in file:
            for word in line.split():
                cleanWord = cleaningOfWord(word)
                if cleanWord is not None:
                    Matrix[wordDict[cleanWord], x] +=1


print Matrix

