import random
import numpy as np
import os
import pickle

from search_config import CLUST_DIR
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D
count=0

def assign_to_clusters(elements, centroids):
    '''
    For each element find the best cluster to assign to.
    :param elements: objects to cluster
    :param centroids: collection of centroids
    :return: dictionary of clusters
    '''
    clusters  = defaultdict(list)

    for x in elements:
        clIndex = min([(i[0], np.linalg.norm(x-centroids[i[0]])) for i in enumerate(centroids)], key=lambda t:t[1])[0]
        clusters[clIndex].append(x)
    return clusters

def assign_indexes_to_clusters(elems, centroids):

    clusters = defaultdict(list)

    for ind, x in enumerate(elems):
        clIndex = min([(i[0], np.linalg.norm(x-centroids[i[0]])) for i in enumerate(centroids)], key=lambda t:t[1])[0]
        clusters[clIndex].append(ind)
    return clusters


def eval_centroids(clusters):
    '''

    :param clusters: dictionary with clustered points as values
    :return: new centroids
    '''
    newCentroids = []
    keys = sorted(clusters.keys())
    for k in keys:
        newCentroids.append(np.mean(clusters[k], axis = 0))
    return newCentroids

def in_minimum(prev, curr):
    '''

    :param prev: centroids from the previous iteration
    :param curr: current centroids
    :return: are we done with iterating - are we in a local minimum
    :rtype: bool
    '''
    global count
    count+=1
    print count


    return (set([tuple(a) for a in curr]) == set([tuple(a) for a in prev]))

def find_centers(elems, k):
    '''
    Lloyd's algorithm implementation. Cluster assignment and centroids evaluation is done alternately.
    :param elems:
    :param k:
    :return:
    '''
    prev = random.sample(elems, k)
    curr = random.sample(elems, k)
    while np.array_equal(prev, curr):
        curr = random.sample(elems, k)
    while not in_minimum(prev, curr):
        prev = curr
        clusters = assign_to_clusters(elems, curr)
        curr = eval_centroids(clusters)
    return curr, clusters


def get_document_clustering(docs, initial= True, nrOfClusters=12):
    if initial:
        if os.path.exists(CLUST_DIR):
            with open(CLUST_DIR, 'rb') as handle:
                return pickle.load(handle)

    centr, clust = find_centers(docs, nrOfClusters)
    clusters =  assign_indexes_to_clusters(docs, centr)

    if initial:
        with open(CLUST_DIR, 'wb') as handle:
            pickle.dump(clusters, handle)
    return clusters

