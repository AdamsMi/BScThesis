__author__ = 'dominikmajda'

import urllib2
from bs4 import BeautifulSoup
import re
from Queue import Queue
from datetime import datetime
import socket

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match(r'<!--.*-->|<!.*|',element.encode('utf-8')):
        return False
    return True


class BaseCrawler(object):
    """
    Simple interface for all crawlers.
    Responsible for creating SOUP object and storing url and html.
    Crawlers should implement downloaded_files method of this class
    """

    def __init__(self, url, date):
        object.__init__(self)
        self.url = url
        try:
            response = urllib2.urlopen(self.url, timeout=10)
            self.html = response.read()
        except urllib2.HTTPError:
            self.html = '<html></hmtl>'
        except socket.timeout:
            self.html = '<html></hmtl>'
        except socket.error:
            self.html = '<html></hmtl>'
        except urllib2.URLError:
            self.html = '<html></hmtl>'

        self.soup = BeautifulSoup(self.html, from_encoding="utf-8")
        self.date = date


    def dump(self, filename, add_links=False, verbose=False):
        """
        Dumps text from website. This method is personalized for specific site
        :param filename: file, where downloaded_files will be saved
        :param add_links: if True website link will be added to downloaded_files
        :param verbose: if True more info will be given in console
        :return True if file was created, False otherwise
        """
        raise NotImplementedError( "Should have implemented this" )


class BaseManager(object):
    """
    Responsible for filling queue with links and returning new Crawler connected with website.
    """

    def __init__(self, date=datetime.now()):
        object.__init__(self)
        # Init queue and news date
        self.queue = Queue()
        self.date = date


    def get_next_link(self, verbose=False):
        """
        Get next crawler with link from this site.
        :param verbose: if True more info will be given in console
        :return: class of BaseCrawler, filled with website info
        """
        raise NotImplementedError( "Should have implemented this" )


    def get_all_article_links(self, url, verbose=False):
        """
        Get all website links on given website. It can be news or archive, subclass should specified
        how to gather all those links.
        :param url: website address of archive site or news site
        :param verbose: if True more info will be given in console
        :return: array with all found links
        """
        raise NotImplementedError( "Should have implemented this" )

    def put_crawler(self, crawler):
        self.queue.put(crawler.html)
