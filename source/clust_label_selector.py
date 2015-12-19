"""
Module selecting top 3 categories for each cluster from k-means clustering.
"""
import pickle
from search_config import DIR_CLUST_CENTROIDS, DIR_TOPIC_CODES
from reuters_centroid_creator import readCategoriesFromFile

def select3BestCategoriesPerCluster(simils):
    dictsToTuples = [[a.keys()[0], a.values()[0]] for a in simils]
    return sorted(dictsToTuples, key= lambda x : x[1], reverse=True)[:3]


catMap = dict(readCategoriesFromFile(DIR_TOPIC_CODES))

with open(DIR_CLUST_CENTROIDS + 'res', 'rb') as input:
    dictOfRes = pickle.load(input)
ans = {}
for clustNr, similarities in dictOfRes.items():
    bestChoices = select3BestCategoriesPerCluster(similarities)
    for x in bestChoices:
        x[0] = catMap[x[0]]
    ans[clustNr] = bestChoices
print ans
with open(DIR_CLUST_CENTROIDS + 'res_limited', 'wb') as output:
    pickle.dump(ans, output)
