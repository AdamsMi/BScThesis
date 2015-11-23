"""
Liczenie centroidow dla 12 klastrow i zapisywanie ich
"""


import pickle
from search_engine import SearchClient
from k_means import get_document_clustering
from search_config import DIR_CLUST_CENTROIDS
import numpy as np
from source.database_manager import DatabaseManager

def calculateCentroidForDocuments(listOfDocNumbers):

    articlesInCluster =  len(listOfDocNumbers)
    centroidCreatedOfFirstArticle = searchClient.matrix[:, listOfDocNumbers[0]]
    for x in listOfDocNumbers[1:]:
        centroidCreatedOfFirstArticle+=searchClient.matrix[:, x]

    return centroidCreatedOfFirstArticle/float(articlesInCluster)


searchClient = SearchClient()
clus = get_document_clustering(np.transpose(searchClient.matrix))

for k, v in clus.items():
    print 'calculating centroid for cluster: ', k
    centroid = calculateCentroidForDocuments(v)
    with open(DIR_CLUST_CENTROIDS + str(k), 'wb') as handle:
        pickle.dump(centroid, handle)
