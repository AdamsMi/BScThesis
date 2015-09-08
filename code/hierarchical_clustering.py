

from scipy import spatial
import fastcluster
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
data = [
    [1.0, 1.2 , 1.4],
    [0.9, 1.25 , 1.6],
    [3.2, 1.2 , 7],
    [3.0, 1.5 , 5]
]


distance = spatial.distance.pdist(data)


linkage = fastcluster.linkage(distance,method="complete")



plt.clf()

ddata = dendrogram(linkage, color_threshold=1, labels=["a", "b", "c", "d"])

plt.show()
