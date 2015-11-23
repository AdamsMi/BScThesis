import os
import pickle
import scipy
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from search_config import DIR_FILES_REUTERS, DIR_MATRIX, DIR_BOWS

def getSavedThings(directory):

    with open(directory + 'amountOfWords.pkl', 'rb') as inputFile:
        amountOfWords = pickle.load(inputFile)

    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)

    return amountOfWords, mapOfWords


def createBagOfWords(vector, amountOfTerms, dictionary):
    bagOfWords = lil_matrix((1, amountOfTerms), dtype=float)
    print vector
    #bagOfWords = np.zeros((amountOfTerms, 1), float)
    for x in vector:
        try:
            ind = dictionary[x]
            bagOfWords[0, ind] += 1
        except:
            continue
    return csr_matrix(bagOfWords, dtype=float)



amount, mapWords = getSavedThings(DIR_MATRIX)
bow = createBagOfWords(open(DIR_FILES_REUTERS+'104566newsML').read().split(), amount, mapWords)
print bow
c = 0
#
# shown = False
# for fileName in os.listdir(DIR_FILES_REUTERS)[127000:]:
#     c+=1
#     ctE = 0
#     if c%500 == 0:
#         print c
#     if ctE %100:
#         if not shown:
#             print 'skipped: ', ctE
#         shown = True
#     if 'newsML' in fileName:
#         if os.path.exists(DIR_BOWS + fileName + '_data.pkl'):
#             ctE+=1
#             shown = False
#         with open(DIR_FILES_REUTERS + fileName) as input:
#             bow = createBagOfWords(input.read().split(), amount, mapWords)
#             path = DIR_BOWS + fileName
#             with open(path + '_data.pkl', 'wb') as output:
#                 pickle.dump(bow.data, output)
#
#             with open(path + '_ind.pkl', 'wb') as output:
#                 pickle.dump(bow.indices, output)
#
#             with open(path + '_ptr.pkl', 'wb') as output:
#                 pickle.dump(bow.indptr, output)
#
#



