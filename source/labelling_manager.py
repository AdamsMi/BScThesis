
'''
This module calculates similarity between a cluster's centroid and category's centroid
 for every k-means cluster and every reuters' category.
'''

import os
import pickle

from search_config      import DIR_CENTROIDS
from scipy.sparse       import csc_matrix
from search_config      import DIR_CLUST_CENTROIDS
from collections import defaultdict

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

dictOfResults = defaultdict(list)
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
            #print x
            with open(DIR_CLUST_CENTROIDS + x) as input:
                clust_centroid = pickle.load(input)
                sum = 0.0
                for ind in a:
                    sum+= curr_centroid[ind,0] * clust_centroid[ind]
                #print sum
                dictOfResults[x].append({ctName : sum})

print dictOfResults

with open(DIR_CLUST_CENTROIDS + 'res', 'wb') as output:
    pickle.dump(dictOfResults, output)