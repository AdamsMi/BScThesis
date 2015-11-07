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

class NewsReuters(object):

    def __init__(self, title, category):
        self.title = title
        self.category=category.split(',')

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

    def put_article(self, url, title, file_name, category = None):
        """
        Puts article info into database
        :param url: article URL
        :param title: article title
        :param file_name: article text file
        :return: True if link was added successfully, False otherwise
        """

        if not category:
            args = (url.decode("utf-8").rstrip(), title.decode("utf-8").rstrip(),
                    file_name.decode("utf-8").rstrip(), None)
        else:
            args = (url.decode("utf-8").rstrip(), title.decode("utf-8").rstrip(),
                    file_name.decode("utf-8").rstrip(), category.decode("utf-8").rstrip())
        c = self.db.cursor()
        try:
            c.execute("INSERT INTO news VALUES (?,?,?,?)", args)
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

class DatabaseManagerReuters(object):

    def __init__(self):
        """
        Creates database and table if not exists
        """

        self.db = sqlite3.connect(DIR_DATABASE + "news_reuters.db")
        self.c = self.db.cursor()

        # Create table if not exists
        tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
        if not self.c.execute(tb_exists).fetchone():
           self.c.execute("CREATE TABLE news (text_file text primary key, title text, category text)")

        # Commit
        self.db.commit()


    def put_article(self, title, file_name, category):
        """
        Puts article info into database
        :param category: article category
        :param title: article title
        :param file_name: article text file
        :return: True if link was added successfully, False otherwise
        """

        args = (file_name.decode("utf-8").rstrip(),
                title.decode("utf-8").rstrip(),
                category.decode("utf-8").rstrip())
        c = self.db.cursor()
        try:
            c.execute("INSERT INTO news(text_file, title, category) VALUES (?,?,?)", args)
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
            row = c.execute("SELECT category, title FROM news WHERE text_file like ?", args).fetchone()
            return NewsReuters(row[1],row[0])
        except:
            return None
        finally:
            c.close()

    def get_connection(self):
        return self.db

    def get_by_category(self, category):

        c = self.db.cursor()
        try:
            result = []
            rows = c.execute("SELECT category, title FROM news WHERE category like '%"+ category +",%'")
            for row in rows:
                result.append(NewsReuters(row[1],row[0]))
            return result
        except:
            return []
        finally:
            c.close()


if __name__ == '__main__':

    databaseReuters = DatabaseManagerReuters()

    news = databaseReuters.get_by_category("C2")

    print news