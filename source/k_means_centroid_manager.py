"""
calculating centroids for a given clustering
"""
import os
import pickle
from search_config import DIR_CLUST_CENTROIDS

def calculateCentroidForDocuments(listOfDocNumbers, matrix):

    articlesInCluster =  len(listOfDocNumbers)
    centroidCreatedOfFirstArticle = matrix[:, listOfDocNumbers[0]]
    for x in listOfDocNumbers[1:]:
        centroidCreatedOfFirstArticle += matrix[:, x]

    return centroidCreatedOfFirstArticle / float(articlesInCluster)

def calculateCentroidsForClustering(clustering, clusteringName, mat):

    for k, v in clustering.items():
        if not os.path.exists(DIR_CLUST_CENTROIDS + 'b' + clusteringName + '_' + str(k)):
            print 'calculating centroid for cluster: ', k
            centroid = calculateCentroidForDocuments(v, mat)
            with open(DIR_CLUST_CENTROIDS + 'b' + clusteringName + '_' + str(k), 'wb') as handle:
                pickle.dump(centroid, handle)
