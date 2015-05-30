__author__ = 'Dominik'


import sqlite3

class DatabaseManager(object):

    def __init__(self):
        """
        Creates database and table if not exists
        """

        self.db = sqlite3.connect("news.db")
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

        args = (url.decode("utf-8"), title.decode("utf-8"), file_name.decode("utf-8"), )
        c = self.db.cursor()
        try:
            c.execute("INSERT INTO news VALUES (?,?,?)", args)
            # Commit
            self.db.commit()
        except sqlite3.IntegrityError:
            c.close()
            self.db.commit()
            return False


        c.close()
        return True

    def get_connection(self):
        return self.db
