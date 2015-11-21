import pickle
import webbrowser

from database_manager   import DatabaseManager
from search_config      import DIR_CENTROIDS
from scipy.sparse       import csc_matrix
from search_config      import DIR_MATRIX
from search_engine      import sparseLowRankAppr

def loadMatrix(directory):
    with open(directory + 'data.pkl', 'rb') as inputFile:
        data = pickle.load(inputFile)

    with open(directory + 'indices.pkl', 'rb') as inputFile:
        indices = pickle.load(inputFile)

    with open(directory + 'indptr.pkl', 'rb') as inputFile:
        indptr = pickle.load(inputFile)

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    with open(directory + 'amountOfFiles.pkl', 'rb') as inputFile:
        amountOfFiles = pickle.load(inputFile)

    with open(directory + 'listOfArticleFiles.pkl', 'rb') as inputFile:
        listOfArticleFiles = pickle.load(inputFile)

    with open(directory + 'idfs.pkl', 'rb') as inputFile:
        idfs = pickle.load(inputFile)

    return csc_matrix((data, indices, indptr)), amountOfFiles, listOfArticleFiles


def fasterCorrelations(matrix, indices, vector,  amountOfDocuments):
    similarities = []
    for x in xrange(amountOfDocuments):
        simil = 0
        for ind in indices:
            simil += matrix[ind,x] * vector[0,ind]
        similarities.append((x, simil))
    return sorted(similarities, key=lambda tup: tup[1], reverse=True)[:3]


class Centroid(object):
    def __init__(self, centroid, catName):
        self.centroid = centroid
        self.catName = catName

    def calcSimilarity(self, bow):
        return self.centroid * bow


with open(DIR_CENTROIDS+ 'C18') as input:
    gwelf_centroid = pickle.load(input)

mtx, amountOfFiles, listOfArticleFiles = loadMatrix(DIR_MATRIX)

mtx = sparseLowRankAppr(mtx, 250)

corr = fasterCorrelations(mtx, gwelf_centroid.nonzero()[1], gwelf_centroid, amountOfFiles)
rs= []
for x in corr:
    print x
    rs.append(listOfArticleFiles[x[0]])

print rs

dbMan = DatabaseManager()

for res in rs:
    webbrowser.open(dbMan.get_link(res).url)