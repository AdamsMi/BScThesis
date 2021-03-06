__author__ = 'ready4s'

import os
import multiprocessing
import time
import sqlite3
import xmltodict

from database_manager import DatabaseManagerReuters
from search_config import DIR_HD_XML, DIR_DATABASE, DIR_FILES
from file_cleaner import chunks, write_to_file, cleaningOfWord

def cleanArticleFormReuters(listOfArticles, pathToArticles, lock):
    dbManager = DatabaseManagerReuters()

    for currentFileName in listOfArticles:

        content = open(DIR_HD_XML + currentFileName, 'r').read()
        articleDict = xmltodict.parse(content)['newsitem']

        articleTopic = ""
        try:
            for topic in articleDict['metadata']['codes']:
                    if topic['@class']=='bip:topics:1.0':
                        try:
                            articleTopic=topic['code']['@code']
                        except:
                            for code in topic['code']:
                                codeName = code["@code"]
                                articleTopic += codeName + ","
        except:
            print "Error in " + currentFileName + ", skipping"
            continue


        articleText = ""
        for line in articleDict['text']['p']:
            if not line==None:
                articleText += " "
                articleText += line

        lock.acquire()
        passed =  dbManager.put_article(articleDict['title'], currentFileName, articleTopic)
        lock.release()

        if passed:

            # Save file to new file
            write_to_file(articleText, pathToArticles + currentFileName.replace('.xml',''))

            # Open it again
            # TODO it shouldn't be opened again
            newFileContent = ""
            currentFile = open(pathToArticles + currentFileName.replace('.xml',''), 'r+')

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


if __name__ == "__main__":
    start = time.time()


    db = sqlite3.connect(DIR_DATABASE + "news_reuters.db")
    c = db.cursor()

    # Create table if not exists
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news_reuters'"
    if not c.execute(tb_exists).fetchone():
       c.execute("CREATE TABLE news_reuters (text_file text primary key, title text, category text)")

    # Commit
    db.commit()
    listOfAlreadyCleaned = os.listdir(DIR_FILES)
    listOfAlreadyCleaned = set([x + '.xml' for x in listOfAlreadyCleaned])
    print 'got set'
    listOfArticles = filter(lambda x: x[0] != '.' and '.zip' not in x,sorted(os.listdir(DIR_HD_XML)))
    print 'got files'
    listOfArticles = filter(lambda x: x not in listOfAlreadyCleaned, listOfArticles)
    print 'amount of articles to clean: ', len(listOfArticles)

    lock = multiprocessing.Lock()
    processes = []

    for chunk in chunks(listOfArticles, 2):
        process = multiprocessing.Process(target=cleanArticleFormReuters, args=(chunk, DIR_FILES, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
