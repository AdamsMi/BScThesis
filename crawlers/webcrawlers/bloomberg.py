import urllib2
from bs4 import BeautifulSoup
import re

from numpy import LineSplitter

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match(r'<!--.*-->|<!.*|',element.encode('utf-8')):
        return False
    return True

class BloombeCrawler(object):

    def __init__(self, url):
        object.__init__(self)
        self.url = url
        response = urllib2.urlopen(self.url)
        self.html = response.read()
        self.soup = BeautifulSoup(self.html, from_encoding="utf-8")
        for string in self.soup.find_all('script'):
            if (string.text.startswith('YMedia.use("media-rmp", "media-viewport-loader"')):
                for string in re.findall(r'<a href=\\"(.*?)<\\\/a>', string.text):
                    # This is crap
                    print re.findall(r'http:(.*?)\?', string)

    def dump(self, filename, add_links=False, verbose=False):
        pass

    @staticmethod
    def get_all_article_links_from_archive(archive_day_url, queue=None, verbose=False):
        pass