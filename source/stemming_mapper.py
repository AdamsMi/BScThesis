import os
import re
import pickle
import numpy

from file_cleaner import cleaningOfWord, get_files_to_clean
from collections import defaultdict
from search_config import DIR_DUMP, DIR_STEMMING_MAP, DIR_CLUST_CENTROIDS, DIR_FREQ_WORDS, DIR_USED_WORDS


def selectTopWordForCoreWord(ansDict, coreWord):
    options = []
    for k, v in ansDict[coreWord].items():
        options.append((k,v))

    if not options:
        return []

    return sorted(options, key = lambda x : x[1], reverse = True)[0][0]

def mappingForSingleArticle(content):
    words = content.split()
    ans = defaultdict(dict)
    for word in words:
        word = re.sub('[^A-Za-z]+', '', word)
        word = word.lower()
        cleanedWord = cleaningOfWord(word)
        if cleanedWord:
            #if cleanedWord not in ans.keys():
            #    ans[cleanedWord] = {}
            if word in ans[cleanedWord].keys():
                ans[cleanedWord][word]+=1
            else:
                ans[cleanedWord][word]=1
    return ans

def calculateAndWriteAllMappings():
    files = get_files_to_clean(DIR_DUMP)
    ct = 0
    for fileName in files:
        ct+=1
        if ct%100==0:
            print ct
        a = mappingForSingleArticle(open(DIR_DUMP + fileName).read())

        with open(DIR_STEMMING_MAP + fileName, 'wb') as out:
            pickle.dump(a, out)

def doesWordAppearInCluster(clustIndexes, core, searchClient):
    for ind in clustIndexes:
        title = searchClient.listOfArticles[ind]
        with open(DIR_STEMMING_MAP + title) as input:
            currMap = pickle.load(input)
        if core in currMap.keys():
            return True
    return False

def getBestWordsForClusterAndCores(clustIndexes, cores, searchClient, dm):
    ans = {}
    for ind in clustIndexes:
        title = searchClient.listOfArticles[ind]
        with open(DIR_STEMMING_MAP + title) as input:
            currMap = pickle.load(input)
        for core in cores:
            if core in ans.keys():
                for k in currMap[core].keys():
                    if k in ans[core].keys():
                        ans[core][k]+=currMap[core][k]
                    else:
                        ans[core][k] = currMap[core][k]
            else:
                ans[core] = currMap[core]
    return [selectTopWordForCoreWord(ans, core) for core in cores if core]


def saveAlreadyUsedWords(drillDownPath, mapping, alreadyUsed):
    for k,v in mapping.items():
        with open(DIR_USED_WORDS + 'b' + drillDownPath + '_' + str(k), 'wb') as output:
            pickle.dump(v + alreadyUsed, output)


def getFreqWordsForClustering(clust, dictOfWords, drillDownPath, searchClient, dm):

    if os.path.exists(DIR_FREQ_WORDS + 'b' + drillDownPath):
        with open(DIR_FREQ_WORDS + 'b' + drillDownPath, 'rb') as input:
            return pickle.load(input)
    if drillDownPath != '':
        with open(DIR_USED_WORDS + 'b' + drillDownPath, 'rb') as input:
            alreadyUsed = pickle.load(input)
    else:
        alreadyUsed = []
    ansOfCores = {}
    ans = {}
    for k, v in clust.items():
        print 'calculating {a} cluster'.format(a=k)
        wordsForClust = []

        with open(DIR_CLUST_CENTROIDS + 'b' + drillDownPath+ '_' + str(k)) as input:
            clust_centroid = pickle.load(input)

        while len(wordsForClust) < 4:
            ind = numpy.argmax(clust_centroid)
            for a,b in dictOfWords.items():
                if b == ind:
                    if a not in alreadyUsed and doesWordAppearInCluster(v, a, searchClient):
                        wordsForClust.append(a)
                        break
                    else:
                        break
            clust_centroid[ind] = min(clust_centroid)

        ansOfCores[k] = wordsForClust
        print wordsForClust
        res = getBestWordsForClusterAndCores(v, wordsForClust, searchClient, dm)
        res = filter(lambda x: x, res)
        print res
        ans[k] = res

    saveAlreadyUsedWords(drillDownPath, ansOfCores, alreadyUsed)

    with open(DIR_FREQ_WORDS + 'b' + drillDownPath, 'wb') as output:
        pickle.dump(ans, output)
    return ans