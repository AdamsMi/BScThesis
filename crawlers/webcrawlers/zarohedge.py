__author__ = 'dominikmajda'

from crawler import BaseCrawler, BaseManager
import urllib2
from bs4 import BeautifulSoup
from datetime import timedelta
import re

class ZeroHedgeCrawler(BaseCrawler):
    """
    Subclass of BaseCrawler for ZeroHedge news.
    """

    def dump(self, filename, add_links=False, verbose=False):

        # Documentation in BaseCrawler

        if verbose:
            print "Dumping " + self.url

        # Gather all texts
        node = self.soup.find_all("div", {"class": "node"})

        if not node or not node[0].find_all("div", {"class": "content"}):
            return False

        content = node[0].find_all("div", {"class": "content"})


        # Save to file
        file = open(filename, 'w')


        # Add links if user wants them
        if add_links:
            file.write(self.url + '\n')

        title = self.soup.title.text.lstrip().encode('utf-8')
        file.write(title + '\n')
        text_to_write = content[0].text
        text_to_write = re.sub(r'\n+', r'\n', text_to_write)
        file.write(text_to_write.lstrip().encode('utf-8'))
        file.close()

        return True


class ZeroHedgeManager(BaseManager):

    def get_next_link(self, verbose=False):

        # Get new links if queue is empty
        if self.queue.empty():
            link = self.next_archive_link(verbose)
            links = self.get_all_article_links(link, verbose = False)

            if (verbose):
                print 'Found links: ' + str(len(links))

        return ZeroHedgeCrawler(self.queue.get(), self.date)

    def next_archive_link(self, verbose=False):

        # Build new archive link

        self.date = self.date - timedelta(days=1)
        stringData = str(self.date.year) + '/' + str(self.date.month) + '/' + str(self.date.day)

        if(verbose):
            print 'Date of archive ' + stringData

        link = 'http://www.zerohedge.com/archive/all/' + stringData
        return link


    def get_all_article_links(self, url, verbose=False):

        # Documentation in BaseCrawler

        links = []

        # Main page
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, from_encoding="utf-8")
        stringData = str(self.date.year) + '/' + str(self.date.month) + '/' + str(self.date.day)

        # Get page archive count
        pages = soup.find('li', { "class" : "pager-last last" })
        page = pages.find('a')['href'].replace('/archive/all/' + stringData + '?page=', '')

        for i in xrange(0, int(page)+1):

            if (verbose):
                print "Archive page " + str(i)

            response = urllib2.urlopen(url + "?page=" + str(i))
            html = response.read()
            soup = BeautifulSoup(html, from_encoding="utf-8")

            for link in soup.find_all('a', href=True):


                if link['href'].startswith('/news/') and link.parent['class'][0] == 'title':
                    links.append('http://www.zerohedge.com' + link['href'])

                    # Print links if verbose
                    if verbose:
                        print link['href']

                    # Add to queue if given
                    if self.queue:
                        self.queue.put('http://www.zerohedge.com' + link['href'])

        return links

