from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from DatabaseManager import DatabaseManager
import re
import os
import multiprocessing
import time
import sqlite3

stemmer = SnowballStemmer('english')
directoryOfDataset = 'files/'
directoryOfDump = 'crawlers/dump/'

def write_to_file(content, new_file_name):
    new_file = open(new_file_name, 'w')
    new_file.write(content)
    new_file.close()

def chunks(l, n):
    newn = int(len(l) / n)
    for i in xrange(0, n-1):
        yield l[i*newn:i*newn+newn]
    yield l[n*newn-newn:]

def structureCleaning(fileName):
    news = open(directoryOfDump + fileName, 'r')
    lineNr = 0
    fullLineCount = 0;
    url = ""; title = "";
    content = ""

    # Read lines data
    for line in news.readlines():
        if lineNr==0:
            url = line
        elif lineNr==1:
            title = line
        elif not line=="\n":
            # Clean here
            if len(line)<40:
                line = line.rstrip()
            content += line.lstrip()
            fullLineCount += 1

        lineNr += 1


    if len(content)<150:
        return None;
    if fullLineCount<3:
        return None;

    return (url, title, content)



def cleaningOfWord(wordBeingCleaned):

    wordBeingCleaned = wordBeingCleaned.lower()
    wordBeingCleaned = re.sub('[^A-Za-z0-9]+', '', wordBeingCleaned)
    if wordBeingCleaned in stopwords.words('english') or 'http' in wordBeingCleaned or 'www' in wordBeingCleaned or (sum(c.isalpha() for c in wordBeingCleaned) >2 and sum(c.isdigit() for c in wordBeingCleaned) ) > 2 :
        return None

    word = stemmer.stem(wordBeingCleaned).encode('ascii', 'english')
    return word if word != '' else None


def cleanAllWordsFromArticles(listOfArticles, pathToArticles, lock):
    dbManager = DatabaseManager()

    for currentFileName in listOfArticles:

        # Start with structure cleaning
        args = structureCleaning(currentFileName)
        if not args==None:
            lock.acquire()
            passed =  dbManager.put_article_with_args(args)
            lock.release()

            if passed:

                # Save file to new file
                write_to_file(args[2], pathToArticles + currentFileName)

                # Open it again
                # TODO it shouldn't be opened again
                newFileContent = ""
                currentFile = open(pathToArticles + currentFileName, 'r+')

                # Use nltk
                for line in currentFile:
                    for word in line.split():
                        cleanedWord = cleaningOfWord(word)
                        if cleanedWord is not None:
                            newFileContent+=cleanedWord +" "

                # Write new content of file
                currentFile.seek(0)
                currentFile.write(newFileContent)
                currentFile.truncate()
                currentFile.close()
            else:
                print "Duplicate file: " + currentFileName
        else:
            print "Wrong structure, denied file: " + currentFileName
            os.remove(directoryOfDump + currentFileName)

    return len(listOfArticles)

if __name__ == "__main__":
    start = time.time()


    db = sqlite3.connect("news.db")
    c = db.cursor()

    # Create table if not exists
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
    if not c.execute(tb_exists).fetchone():
       c.execute("CREATE TABLE news (url text primary key, title text, text_file text)")

    # Commit
    db.commit()

    listOfArticles = os.listdir(directoryOfDump)
    lock = multiprocessing.Lock()
    processes = []

    for chunk in chunks(listOfArticles, 2):
        process = multiprocessing.Process(target=cleanAllWordsFromArticles, args=(chunk, directoryOfDataset, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    stop = time.time()
    print "Time spent: ", stop-start
