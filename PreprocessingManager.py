__author__ = 'Michal'

import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re


directoryOfDataset = 'files/'
stemmer = SnowballStemmer('english')


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

if __name__ == 'main':


    listOfArticleFiles = os.listdir(directoryOfDataset)
    setOfWords = gatherAllWordsFromArticles(listOfArticleFiles, directoryOfDataset)