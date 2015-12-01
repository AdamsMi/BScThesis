"""
Module calculating bow for reuters files and dumping them as csr_matrix.
"""


import os
import pickle
from scipy.sparse import lil_matrix, csr_matrix
from search_config import DIR_FILES_REUTERS, DIR_MATRIX, DIR_BOWS

STEPINFO = True

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


if __name__ == '__main__':
    amount, mapWords = getSavedThings(DIR_MATRIX)
    if STEPINFO:
        c = 0

    shown = False
    for fileName in os.listdir(DIR_FILES_REUTERS):
        if STEPINFO:
            c+=1
            if c%500 == 0:
                print c
        if 'newsML' in fileName:
            if os.path.exists(DIR_BOWS + fileName + '_data.pkl'):
                shown = False
            with open(DIR_FILES_REUTERS + fileName) as input:
                bow = createBagOfWords(input.read().split(), amount, mapWords)
                path = DIR_BOWS + fileName
                with open(path + '_data.pkl', 'wb') as output:
                    pickle.dump(bow.data, output)

                with open(path + '_ind.pkl', 'wb') as output:
                    pickle.dump(bow.indices, output)

                with open(path + '_ptr.pkl', 'wb') as output:
                    pickle.dump(bow.indptr, output)





