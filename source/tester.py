import pickle
from search_config import DIR_CLUST_CENTROIDS

def calculateSimilarityBetweenQueryAndCentroid(query, centroid):
    sim = 0.0
    a,b = query.nonzero()
    for ind in b:
        sim += centroid[ind] * query[0,ind]
    return sim

def getBestClustersForQuery(query, nrOfClusters = 3):
    a = []
    for k in xrange(12):
        with open(DIR_CLUST_CENTROIDS + str(k)) as input:
            clust_centroid = pickle.load(input)
            a.append([k, calculateSimilarityBetweenQueryAndCentroid(query=query, centroid=clust_centroid)])
    return sorted(a, key = lambda x: x[1], reverse = True)[:nrOfClusters]