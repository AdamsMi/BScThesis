from source import preprocessing_manager

__author__ = 'Michal'


import unittest


mockFile1 = [['this is example'],['very interesting example'],['article about football'],['left winger does not have a home']]
mockFile2 = [['this line is about nothing'],['just a little more precise'],['thank you for quick turnaround']]
filesList = [mockFile1, mockFile2]


class TestPreprocessing(unittest.TestCase):

    def test_normalization(self):
        import numpy as np
        mat = np.random.rand(6,6)
        mat = preprocessing_manager.normalization(mat, 6)
        print mat
        for i in xrange(6):
            diff = abs( sum(mat[:,i]**2) - 1)
            print diff
            self.assertTrue( diff < 0.01 )


    def test_idf(self):
        import numpy as np
        articlesNr = 2
        wordList = ['this', 'is', 'a', 'sample', 'another', 'example']
        occDict = {
            'this': 2,
            'is': 2,
            'a': 1,
            'sample': 1,
            'another': 1,
            'example': 1
        }

        matr = np.matrix([
            [1.0, 1.0],
            [1.0, 1.0],
            [2.0, 0.0],
            [1.0, 0.0],
            [0.0, 2.0],
            [0.0, 3.0]
        ])

        outcM, outcIdfs =  preprocessing_manager.idf(matr, articlesNr, occDict, wordList)
        self.assertTrue(np.allclose(outcM, [[0,0],[0,0],[0.6020599,0],[0.30103,0],[0,0.6020599],[0,0.9030899]]))



def test_gatherAllWords():
    words, dictOfWords, matrix, dictOfTermOccurrences, mapOfWords = preprocessing_manager.gatherAllWordsFromArticles( ['file', 'file2'], './testfiles')
    print 'words', words
    print 'dictOfWords', dictOfWords
    print 'matrix', matrix
    print 'dictOfTermOccurences', dictOfTermOccurrences
    print 'map of words: ', mapOfWords



#if __name__ == '__main__':
    #unittest.main()
test_gatherAllWords()