import os
import pickle
import numpy as np
from search_config      import DIR_TOPIC_CODES, DIR_FILES, DIR_MATRIX, DIR_CENTROIDS, DIR_CENTROIDS_NGRAMS

currDone = os.listdir(DIR_CENTROIDS_NGRAMS)
currDoneNgrams = os.listdir(DIR_CENTROIDS)

for centroid in currDone:
    if centroid in currDoneNgrams:
        print "Connecting centroid: ", centroid


        with open(DIR_CENTROIDS_NGRAMS + centroid, 'rb') as centroidNgram:
            centroidNgram = pickle.load(centroidNgram)


            with open(DIR_CENTROIDS + centroid, 'rb') as centroidBow:
                centroidBow = pickle.load(centroidBow)

                print "Centroid shape before: ", centroidBow.shape

                np.append(centroidBow, centroidNgram)

                print "Centroid shapre after: ", centroidBow.shape


    else:
        print "No cetnroid for: ", centroid