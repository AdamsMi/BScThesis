__author__ = 'Michal'

import os



# Here:
# - remove numbers and special characters
# - take only a core of a given word
# - remove stop words
# - lowercase

def cleaningOfWord(wordBeingCleaned):
    return wordBeingCleaned

def gatherAllWordsFromArticles(listOfArticles, pathToArticles):
    words = set()

    for currentFileName in listOfArticles:
        currentFile = open(pathToArticles + currentFileName)
        for line in currentFile:
            for word in line.split():
                cleanedWord = cleaningOfWord(word)
                if len(cleanedWord)> 0:
                    words.add(cleanedWord)
        currentFile.close()

if __name__ == 'main':

    listOfArticleFiles = os.listdir('files/')
    gatherAllWordsFromArticles(listOfArticleFiles, 'files/')