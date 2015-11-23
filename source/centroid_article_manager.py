import os
from search_config import DIR_CENTROIDS2, DIR_CLUST_CENTROIDS
import pickle
from k_means import get_document_clustering
from search_engine import SearchClient
from source.database_manager import DatabaseManager


def calcCentroid(matrix, indices):
    startingPoint = matrix[:, indices[0]]
    print startingPoint
    for ind in indices[1:]:
        startingPoint += matrix[:, ind]
        print matrix[:, ind]
    return startingPoint / float(len(indices))

def findArticleClosestToCentroid(listOfDocNumbers, centroid, mtx):
    a = []
    sim = 0.0
    for x in listOfDocNumbers:
        for ind in xrange(len(centroid)):
            sim += centroid[ind] * mtx[ind, x]
        a.append((x,sim))
        sim = 0.0
    return sorted(a, key = lambda x: x[1], reverse=True)[0]

if __name__ == '__main__':
    searchClient = SearchClient()
    dm = DatabaseManager()
    answerDict = {}
    clus = get_document_clustering(None)
    for k, v in clus.items():
        with open(DIR_CLUST_CENTROIDS + str(k)) as input:
            clust_centroid = pickle.load(input)
        print 'working on cluster: ', k
        bestArticle = findArticleClosestToCentroid(v, clust_centroid, searchClient.matrix)
        print 'best: ', bestArticle
        title = searchClient.listOfArticles[bestArticle[0]]
        ans = dm.get_link(title).title
        print ans
        answerDict[k]=ans

    with open(DIR_CLUST_CENTROIDS + 'closestArt','wb') as out:
        pickle.dump(answerDict, out)
    print answerDict