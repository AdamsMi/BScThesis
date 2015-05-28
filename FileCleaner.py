from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import re
import os
import multiprocessing
import time

stemmer = SnowballStemmer('english')
directoryOfDataset = 'files/'

def chunks(l, n):
    newn = int(len(l) / n)
    for i in xrange(0, n-1):
        yield l[i*newn:i*newn+newn]
    yield l[n*newn-newn:]


def cleaningOfWord(wordBeingCleaned):

    wordBeingCleaned = wordBeingCleaned.lower()
    wordBeingCleaned = re.sub('[^A-Za-z0-9]+', '', wordBeingCleaned)
    if wordBeingCleaned in stopwords.words('english') or 'http' in wordBeingCleaned or 'www' in wordBeingCleaned or (sum(c.isalpha() for c in wordBeingCleaned) >2 and sum(c.isdigit() for c in wordBeingCleaned) ) > 2 :
        return None

    word = stemmer.stem(wordBeingCleaned).encode('ascii', 'english')
    return word if word != '' else None


def cleanAllWordsFromArticles(listOfArticles, pathToArticles):
    for currentFileName in listOfArticles:
        newFileContent = ""

        currentFile = open(pathToArticles + currentFileName, 'r+')

        for line in currentFile:
            for word in line.split():
                cleanedWord = cleaningOfWord(word)
                if cleanedWord is not None:
                    newFileContent+=cleanedWord +" "
        currentFile.seek(0)
        currentFile.write(newFileContent)
        currentFile.truncate()
        currentFile.close()
    return len(listOfArticles)

if __name__ == "__main__":
    start = time.time()
    listOfArticles = os.listdir(directoryOfDataset)
    pool = multiprocessing.Pool(processes = 2)
    results = [pool.apply_async(cleanAllWordsFromArticles, args=(x, directoryOfDataset,)) for x in chunks(listOfArticles, 2)]
    output = [p.get() for p in results]
    print(output)

    stop = time.time()
    print "Time spent: ", stop-start
