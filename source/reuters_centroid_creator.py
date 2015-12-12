import os
import pickle
import math
import time
import numpy
from database_manager   import DatabaseManagerReuters
from scipy.sparse       import csr_matrix, csc_matrix
from search_config      import DIR_TOPIC_CODES, DIR_FILES, DIR_MATRIX, DIR_CENTROIDS, DIR_CENTROIDS_NGRAMS
from search_config      import DIR_BOWS
dbManager = DatabaseManagerReuters()


def getSavedThings(directory):

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    with open(directory + 'articleInvariants.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return amountOfWords, mapOfWords, idfs


def getSavedBow(fileName):
    path = DIR_BOWS + fileName
    with open(path + '_data.pkl', 'rb') as input:
        data = pickle.load(input)

    with open(path + '_ind.pkl', 'rb') as input:
        ind = pickle.load(input)

    with open(path + '_ptr.pkl', 'rb') as input:
        ptr = pickle.load(input)
    try:
        m= csr_matrix((data, ind, ptr))
    except ValueError:
        print fileName
        return None
    return m

def saveCentroidOfCategory(centroid, catName):
    '''
    Save a calculated centroid.
    :param centroid: calculated centroid
    :param catName: category name
    '''
    if  ngramsCentroids:
        with open(DIR_CENTROIDS_NGRAMS + catName, 'wb') as writeFile:
            pickle.dump(centroid, writeFile)
    else:
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
    a = []
    for cat in cats:
        articlesPerCat = dbManager.get_by_category(cat[0])
        if len(articlesPerCat) >0:
            a.append([cat[0], len(articlesPerCat)])
    return a


def calcIdf(bow, idfs, amountOfWords):
    ct=0
    for x in xrange(amountOfWords):
        if bow[x,0]>0:
            ct+=1
            bow[x,0] *= idfs[x]
    print 'nonzeros: ', ct

    return bow

def createCentroidForCategory(category):
    filesAboutCategory = dbManager.get_by_category(category)
    amountOfWords, dictOfWords, idfs, ngrams = getSavedThings(DIR_MATRIX)

    a = numpy.zeros((amountOfWords, 1), float)
    aOfFiles = len(filesAboutCategory)
    for fileName in filesAboutCategory:
        fileName = str(fileName).replace('.xml', '')
        bow = getSavedBow(fileName)
        if bow is None:
            print 'skipped', fileName
            aOfFiles -=1
            continue
        c,b = bow.nonzero()
        for x in b:
            a[x,0] += bow[0,x]

    return calcIdf(a, idfs, amountOfWords) / float(aOfFiles)


def normalizeCentroid(centroid):
    s=0
    ind, nonzeros = centroid.nonzero()
    for x in ind:
        s += centroid[x,0] * centroid[x,0]
    centroid /= math.sqrt(s)
    s=0
    for x in ind:
        s += centroid[x,0] * centroid[x,0]
    return centroid


def createNgramCentroidForCategory(category):
    filesAboutCategory = dbManager.get_by_category(category)
    amountOfWords, dictOfWords, idfs, ngrams = getSavedThings(DIR_MATRIX)

    centroid = numpy.zeros(6)
    aOfFiles = len(filesAboutCategory)

    for fileName in filesAboutCategory:
        index = listOfArticleRouterFiles.index(fileName)
        invariants = ngrams[index]
        for i in xrange(0,6):
            centroid[i] += invariants[i]

    return centroid/aOfFiles



if __name__ == '__main__':

    ngramsCentroids = True

    cats = getArticlesForAllCategories()

    if ngramsCentroids:
        currDone = os.listdir(DIR_CENTROIDS_NGRAMS)
    else:
        currDone = os.listdir(DIR_CENTROIDS)

    for cat in cats:
        if cat[0] not in currDone:
            if cat[1]>0:

                start = time.time()
                if ngramsCentroids:
                    print 'creating ngram centroid for category', cat[0], ': ', cat[1]
                    listOfArticleRouterFiles = filter(lambda x: x[0] != '.',sorted(os.listdir(DIR_FILES)))
                    centroid = createNgramCentroidForCategory(cat[0])
                    saveCentroidOfCategory(centroid, cat[0])
                else:

                    print 'creating centroid for category: ', cat[0], ': ', cat[1]
                    ans = createCentroidForCategory(cat[0])
                    ans = csc_matrix(ans)
                    ans = normalizeCentroid(ans)
                    saveCentroidOfCategory(ans, cat[0])

                print 'finished, took: ', time.time() - start
        else:
            print "Done:, ", cat[0]