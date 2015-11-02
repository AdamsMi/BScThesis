__author__ = 'ready4s'

import re
import os
import multiprocessing
import time
import sqlite3
import xmltodict

from database_manager import DatabaseManager
from search_config import DIR_XML, DIR_DATABASE, DIR_FILES
from file_cleaner import chunks, write_to_file, cleaningOfWord

def cleanArticleFormReuters(listOfArticles, pathToArticles, lock):
    dbManager = DatabaseManager()

    for currentFileName in listOfArticles:

        content = open(DIR_XML + currentFileName, 'r').read()
        articleDict = xmltodict.parse(content)['newsitem']

        articleTopic = None
        try:
            for topic in articleDict['metadata']['codes']:
                    if topic['@class']=='bip:topics:1.0':
                        try:
                            articleTopic=topic['code'][0]['@code']
                        except:
                            articleTopic=topic['code']['@code']
        except:
            continue

        articleText = ""
        for line in articleDict['text']['p']:
            articleText += " "
            articleText += line

        lock.acquire()
        passed =  dbManager.put_article(articleDict['@itemid'], articleDict['title'], currentFileName, articleTopic)
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


    db = sqlite3.connect(DIR_DATABASE + "news.db")
    c = db.cursor()

    # Create table if not exists
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
    if not c.execute(tb_exists).fetchone():
       c.execute("CREATE TABLE news (url text primary key, title text, text_file text, category text)")

    # Commit
    db.commit()
    listOfArticles = filter(lambda x: x[0] != '.',sorted(os.listdir(DIR_XML)))


    lock = multiprocessing.Lock()
    processes = []

    for chunk in chunks(listOfArticles, 2):
        process = multiprocessing.Process(target=cleanArticleFormReuters, args=(chunk, DIR_FILES, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
