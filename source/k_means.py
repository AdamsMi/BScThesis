'''
Lloyd's k-means algorithm with a special points' initialization (so-called k-means++)
'''

from copy import copy
import random
import numpy as np
import os
import pickle

from search_config import CLUST_DIR
from collections import defaultdict
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

def nearest_cluster_center(point, centroids):
    cl = min([(i[0], np.linalg.norm(point-centroids[i[0]])) for i in enumerate(centroids)], key=lambda t:t[1])
    return cl


def kpp(points, centersNr):
    cluster_centers = [copy(random.choice(points))]
    d = [0.0 for _ in xrange(len(points))]

    for i in xrange(1, centersNr):
        sum = 0
        for j, p in enumerate(points):
            d[j] = nearest_cluster_center(p, cluster_centers[:i])[1]
            sum += d[j]

        sum *= random.random()

        for j, di in enumerate(d):
            sum -= di
            if sum > 0:
                continue
            cluster_centers.append(copy(points[j]))
            break

    return cluster_centers





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

    if prev is None:
        return False

    return (set([tuple(a) for a in curr]) == set([tuple(a) for a in prev]))

def find_centers(elems, k):
    '''
    Lloyd's algorithm implementation. Cluster assignment and centroids evaluation is done alternately.
    :param elems:
    :param k:
    :return:
    '''
    curr = kpp(elems, k)
    prev = None

    while not in_minimum(prev, curr):
        prev = curr
        clusters = assign_to_clusters(elems, curr)
        curr = eval_centroids(clusters)
    return curr, clusters


def get_document_clustering(docs, fileName = '', nrOfClusters=12, actualIndexes = None):
    """

    :param docs: bows for the articles being clustered
    :param fileName: 'b'(_nrOfCluster)* - identifier of drill-down cluster. b means basic
    :param nrOfClusters: optional, 12 by default
    :param actualIndexes: Indexes of clustered files
    :return: dictionary (nrOfCluster) -> [articles for this nr]
    """

    if os.path.exists(CLUST_DIR + 'b' + fileName + '.pickle'):
        with open(CLUST_DIR + 'b' + fileName + '.pickle',  'rb') as handle:
            return pickle.load(handle)

    centr, clust = find_centers(docs, nrOfClusters)
    clusters =  assign_indexes_to_clusters(docs, centr)
    if actualIndexes is None:
        with open(CLUST_DIR + 'b' + fileName + '.pickle', 'wb') as handle:
            pickle.dump(clusters, handle)
        return clusters
    else:
        print clusters
        print 'dealing with re-indexing...'
        a = {}
        actualIndexes  = sorted(actualIndexes)
        for k in clusters.keys():
            a[k] = [actualIndexes[l] for l in clusters[k]]
        with open(CLUST_DIR + 'b' + fileName + '.pickle', 'wb') as handle:
            print a
            pickle.dump(a, handle)

    return a
