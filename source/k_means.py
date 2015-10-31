import random
import numpy as np
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D


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

def init_board(n):
    X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(n)])
    return X

a = init_board(20)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()


colors = ['green', 'blue', 'brown', 'yellow', 'black']

centr, clust = find_centers(a,4)
v=0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for x in clust.values():
    ax.scatter([el[0] for el in x], [el[1] for el in x], [el[2] for el in x], color=colors[v])
    v+=1

ax.scatter([el[0] for el in centr], [el[1] for el in centr], [el[2] for el in centr], color=colors[v],  s=42, marker=u'*')

plt.show()
print centr
print clust
