
'''
This module calculates similarity between a cluster's centroid and category's centroid
 for every k-means cluster and every reuters' category.
After that, the best 3 Reuters categories are chosen for each cluter.
'''

import os
import pickle

from search_config              import DIR_CENTROIDS
from scipy.sparse               import csc_matrix
from collections                import defaultdict
from search_config              import DIR_CLUST_CENTROIDS, DIR_TOPIC_CODES
from reuters_centroid_creator   import readCategoriesFromFile



def loadMatrix(directory):
    with open(directory + 'data.pkl', 'rb') as inputFile:
        data = pickle.load(inputFile)

    with open(directory + 'indices.pkl', 'rb') as inputFile:
        indices = pickle.load(inputFile)

    with open(directory + 'indptr.pkl', 'rb') as inputFile:
        indptr = pickle.load(inputFile)

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'amountOfFiles.pkl', 'rb') as inputFile:
        amountOfFiles = pickle.load(inputFile)

    with open(directory + 'listOfArticleFiles.pkl', 'rb') as inputFile:
        listOfArticleFiles = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return csc_matrix((data, indices, indptr)), amountOfFiles, listOfArticleFiles

def select3BestCategoriesPerCluster(simils):
    dictsToTuples = [[a.keys()[0], a.values()[0]] for a in simils]
    return sorted(dictsToTuples, key= lambda x : x[1], reverse=True)[:3]


def fasterCorrelations(matrix, indices, vector,  amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = 0
        for ind in indices:
            simil += matrix[ind,x] * vector[0,ind]
        similarities.append((x, simil))
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:3]


centroidList = filter(lambda x : '.' not in x , os.listdir(DIR_CENTROIDS))
print centroidList

dictOfRes = defaultdict(list)
ct = 0
for ctName in centroidList:
    print ctName
    with open(DIR_CENTROIDS + ctName, "rb") as input:
        curr_centroid = pickle.load(input)
    ct+=1
    print len(centroidList) - ct, ' to go'
    a,b = curr_centroid.nonzero()
    for x in os.listdir(DIR_CLUST_CENTROIDS):
        if '.' not in x:
            with open(DIR_CLUST_CENTROIDS + x) as input:
                clust_centroid = pickle.load(input)
                sum = 0.0
                for ind in a:
                    sum+= curr_centroid[ind,0] * clust_centroid[ind]
                dictOfRes[x].append({ctName : sum})


catMap = dict(readCategoriesFromFile(DIR_TOPIC_CODES))

ans = {}
for clustNr, similarities in dictOfRes.items():
    bestChoices = select3BestCategoriesPerCluster(similarities)
    for x in bestChoices:
        x[0] = catMap[x[0]]
    ans[clustNr] = bestChoices
print ans
with open(DIR_CLUST_CENTROIDS + 'res_limited', 'wb') as output:
    pickle.dump(ans, output)