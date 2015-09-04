__author__ = 'Michal'


import unittest

import PreprocessingManager

class TestPreprocessing(unittest.TestCase):

    def test_normalization(self):
        import numpy as np
        mat = np.random.rand(6,6)
        mat = PreprocessingManager.normalization(mat, 6)
        print mat
        for i in xrange(6):
            diff = abs( sum(mat[:,i]**2) - 1)
            #print diffpythonpythoz
            print diff
            self.assertTrue( diff < 0.01 )


if __name__ == '__main__':
    unittest.main()