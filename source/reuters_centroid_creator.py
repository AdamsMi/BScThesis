import os
import pickle

from database_manager   import DatabaseManagerReuters
from scipy.sparse       import lil_matrix
from search_config      import DIR_XML, DIR_TOPIC_CODES, DIR_FILES, DIR_MATRIX
from search_engine      import createBagOfWordsFromVector

listOfArticles = filter(lambda x: x[0] != '.', sorted(os.listdir(DIR_XML)))

dbManager = DatabaseManagerReuters()

def getSavedThings(directory):

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return amountOfWords, mapOfWords, idfs


def splitAndCleanLine(line):
    a = line.split('\t')
    a[1] = a[1].replace('\n', '')
    a[1] = a[1].replace('\r', '')
    return a


def readCategoriesFromFile(dirCodes):
    with open(dirCodes) as codesFile:
        lines = codesFile.readlines()

        return map(splitAndCleanLine, lines)


def getWordsFromFile(path):
    with open(path) as curFile:
        vector = []
        for line in curFile.readlines():
            vector += line.split()
        return vector


def getArticlesForAllCategories():
    cats = readCategoriesFromFile(DIR_TOPIC_CODES)
    print cats
    for cat in cats:
        articlesPerCat = dbManager.get_by_category(cat[0])
        print cat, ' ', len(articlesPerCat)


def createCentroidForCategory(category):
    filesAboutCategory = dbManager.get_by_category(category)
    amountOfWords, dictOfWords, idfs = getSavedThings(DIR_MATRIX)
    for idf in idfs:
        if idf < 0 :
            print idf
    a = None

    for fileName in filesAboutCategory:
        fNStr = str(fileName)
        pathToCleanedFile = DIR_FILES + fNStr.replace('.xml', '')
        words = getWordsFromFile(pathToCleanedFile)[:10]
        indices, _ = createBagOfWordsFromVector(words, amountOfWords, dictOfWords, idfs)
        indices = lil_matrix(indices)
        if a is not None:
            zeros, nonZeroIndices = indices.nonzero()
            for x in nonZeroIndices:
                if x == 131:
                    print pathToCleanedFile
                    print dictOfWords[131]
                a[0, x] += indices[0,x]
        else:
            a = indices
    return a / float(len(filesAboutCategory))

#print createCentroidForCategory('GWELF')
getArticlesForAllCategories()