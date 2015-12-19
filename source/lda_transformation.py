import time
import lda
import numpy as np
import pickle

from scipy.sparse import csc_matrix
from search_config import DIR_INT_MATRIX, DIR_MATRIX

def loadDictOfWords(directory):
    with open(directory + 'mapOfWords.pkl', 'rb') as inputFile:
        mapOfWords = pickle.load(inputFile)
    ans = []
    for k, v in mapOfWords.items():
        ans.append((k,v))
    print ans[:5]
    print 'len of ans: ', len(ans)
    return ans

def loadData(directory):
    with open(directory + 'data.pkl', 'rb') as inputFile:
        data = pickle.load(inputFile)

    inputFile = open(directory + 'indices.pkl', 'rb')
    indices = pickle.load(inputFile)
    inputFile.close()

    inputFile = open(directory + 'indptr.pkl', 'rb')
    indptr = pickle.load(inputFile)
    inputFile.close()


    return csc_matrix((data, indices, indptr))

def getLDAModel():

    matrix = loadData(DIR_INT_MATRIX)

    mapOfWords = loadDictOfWords(DIR_MATRIX)

    mapOfWords = sorted(mapOfWords, key = lambda x: x[1])

    vocab = [a[0] for a in mapOfWords]
  #  print vocab[:5]
  #  print matrix.shape

    matrixToLda = np.transpose(matrix)

  #  print matrixToLda.shape

    start = time.time()

    model = lda.LDA(n_topics=40, n_iter=100, random_state=1)
    model.fit(matrixToLda)



    #
    topic_word = model.topic_word_
    #
    # print time.time() - start
    n =10
    #
    pA = []
    for i, topic_dist in enumerate(topic_word):
        wordsForTopic = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    #    print wordsForTopic
        if i ==10:
     #       print wordsForTopic
            pA = wordsForTopic
    #
    return model, pA
    # doc_topic = model.doc_topic_
    # for n in range(5):
    #     print doc_topic[n]