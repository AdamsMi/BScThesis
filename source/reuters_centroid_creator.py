import pickle
import math

from database_manager   import DatabaseManagerReuters
from scipy.sparse       import lil_matrix
from search_config      import DIR_TOPIC_CODES, DIR_FILES_REUTERS, DIR_MATRIX, DIR_CENTROIDS
from search_engine      import createBagOfWordsFromVector

dbManager = DatabaseManagerReuters()

def getSavedThings(directory):

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return amountOfWords, mapOfWords, idfs


def saveCentroidOfCategory(centroid, catName):
    '''
    Save a calculated centroid.
    :param centroid: calculated centroid
    :param catName: category name
    '''
    with open(DIR_CENTROIDS + catName, 'wb') as writeFile:
        pickle.dump(centroid, writeFile)


def splitAndCleanLine(line):
    a = line.split('\t')
    a[1] = a[1].replace('\n', '')
    a[1] = a[1].replace('\r', '')
    return a


def readCategoriesFromFile(dirCodes):
    '''
    Load all possible categories
    :param dirCodes: directory to categories
    :return: list of lists [categoryCode, category full name]
    '''
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
    nonzero = 0
    zeros = 0
    for cat in cats:
        articlesPerCat = dbManager.get_by_category(cat[0])
        print cat, ' ', len(articlesPerCat)
        if len(articlesPerCat) >0:
            nonzero+=1
        else:
            zeros+=1
    print 'nonzeros: ', nonzero
    print 'zeros', zeros

def createCentroidForCategory(category):
    filesAboutCategory = dbManager.get_by_category(category)
    print 'files for category C18 amount: ', len(filesAboutCategory)
    amountOfWords, dictOfWords, idfs = getSavedThings(DIR_MATRIX)
    for idf in idfs:
        if idf < 0 :
            print idf
    a = None

    for fileName in filesAboutCategory:
        fNStr = str(fileName)
        pathToCleanedFile = DIR_FILES_REUTERS + fNStr.replace('.xml', '')
        print pathToCleanedFile
        words = getWordsFromFile(pathToCleanedFile)
        indices, bow = createBagOfWordsFromVector(words, amountOfWords, dictOfWords, idfs)
        indices = lil_matrix(indices)
        if a is not None:
            zeros, nonZeroIndices = indices.nonzero()
            for x in nonZeroIndices:
                a[0, x] += indices[0,x]
        else:
            a = indices
    return a / float(len(filesAboutCategory)), bow


def normalizeCentroid(centroid, nonzeros):
    for x in bow:
        s += ans[0,x]^2
    print 'sum'
    print s

    ans /= math.sqrt(s)


#ans, bow = createCentroidForCategory('C18')

#print ans

#s = 0
#print ans

#print ans

#saveCentroidOfCategory(ans, 'C18')
getArticlesForAllCategories()

#with open(DIR_CENTROIDS+ 'GREL') as input:
#    gwelf_centroid = pickle.load(input)


#print gwelf_centroid
#print type(gwelf_centroid)
