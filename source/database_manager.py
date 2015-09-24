__author__ = 'Dominik'

import sqlite3

from search_config import DIR_DATABASE

class News(object):

    def __init__(self, url, title):
        self.title = title
        self.url = url

    def serialize(self):
        return {
            "title": self.title,
            "url": self.url
        }

class DatabaseManager(object):

    def __init__(self):
        """
        Creates database and table if not exists
        """

        self.db = sqlite3.connect(DIR_DATABASE + "news.db")
        self.c = self.db.cursor()

        # Create table if not exists
        tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
        if not self.c.execute(tb_exists).fetchone():
           self.c.execute("CREATE TABLE news (url text primary key, title text, text_file text)")

        # Commit
        self.db.commit()

    def put_article_with_args(self, args):
        return self.put_article(args[0], args[1], args[2])

    def put_article(self, url, title, file_name):
        """
        Puts article info into database
        :param url: article URL
        :param title: article title
        :param file_name: article text file
        :return: True if link was added successfully, False otherwise
        """

        args = (url.decode("utf-8").rstrip(), title.decode("utf-8").rstrip(), file_name.decode("utf-8").rstrip(), )
        c = self.db.cursor()
        try:
            c.execute("INSERT INTO news VALUES (?,?,?)", args)
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            c.close()
            self.db.commit()

    def get_link(self, file_name):
        """
        Returns URL address for given file
        :param file_name: file containing news text
        :return: News with URL name and title or None if no such file
        """

        args = (file_name.decode("utf-8"),)
        c = self.db.cursor()
        try:
            row = c.execute("SELECT url,title FROM news where text_file like ?", args).fetchone()
            return News(row[0],row[1])
        except:
            return None
        finally:
            c.close()


    def get_connection(self):
        return self.db
