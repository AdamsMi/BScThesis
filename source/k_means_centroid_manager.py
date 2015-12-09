"""
calculating centroids for a given clustering
"""
import os
import pickle
from search_config import DIR_CLUST_CENTROIDS

def calculateCentroidForDocuments(listOfDocNumbers, matrix, ngramsMatrix):

    articlesInCluster =  len(listOfDocNumbers)
    centroidCreatedOfFirstArticle = matrix[:, listOfDocNumbers[0]]
    ngramsCentroidCreatedOfFirstArticle = ngramsMatrix[:, listOfDocNumbers[0]]
    for x in listOfDocNumbers[1:]:
        centroidCreatedOfFirstArticle += matrix[:, x]
        ngramsCentroidCreatedOfFirstArticle = ngramsMatrix[:, x]


    return centroidCreatedOfFirstArticle / float(articlesInCluster),\
           ngramsCentroidCreatedOfFirstArticle/ float(articlesInCluster)

def calculateCentroidsForClustering(clustering, clusteringName, mat, ngramsMat):

    for k, v in clustering.items():
        if not os.path.exists(DIR_CLUST_CENTROIDS + 'b' + clusteringName + '_' + str(k)):
            print 'calculating centroid for cluster: ', k
            centroid, centroidNgrams = calculateCentroidForDocuments(v, mat, ngramsMat)
            with open(DIR_CLUST_CENTROIDS + 'b' + clusteringName + '_' + str(k), 'wb') as handle:
                pickle.dump(centroid, handle)
