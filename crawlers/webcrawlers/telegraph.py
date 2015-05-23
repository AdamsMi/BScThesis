__author__ = 'dominikmajda'

from crawler import BaseCrawler, BaseManager
import urllib2
from bs4 import BeautifulSoup
from datetime import timedelta

class TelegraphCrawler(BaseCrawler):
    """
    Subclass of BaseCrawler for Telegraph finance news.
    """

    def dump(self, filename, add_links=False, verbose=False):

        # Documentation in BaseCrawler

        if verbose:
            print "Dumping " + self.url

        # Gather all texts
        texts = self.soup.findAll(text=True)
        content = self.soup.find("div", {"id": "mainBodyArea"})

        if not content:
            return False

        # Save to file
        file = open(filename, 'w')

        # Add links if user wants them
        if add_links:
            file.write(self.url + '\n')

        title = self.soup.title.text.lstrip().encode('utf-8')
        file.write(title.replace(' - Telegraph', '\n'))
        for tag in content.find_all('p'):
            if tag.string and tag.string!='\n':
                file.write(tag.string.lstrip().encode('utf-8'))
                file.write('\n')
        file.close()

        return True

class TelegraphManager(BaseManager):

    def get_next_link(self, verbose=False):

        # Get new links if queue is empty
        # TODO if one site has 50 for day, another 20 - it will be faster in the past
        if self.queue.empty():
            link = self.next_archive_link(verbose)
            links = self.get_all_article_links(link, verbose = False)

            if (verbose):
                print 'Found links: ' + str(len(links))

        return TelegraphCrawler(self.queue.get(), self.date)

    def next_archive_link(self, verbose=False):
        # Build new archive link

        self.date = self.date - timedelta(days=1)
        stringData = str(self.date.year) + '-' + str(self.date.month) + '-' + str(self.date.day)

        if(verbose):
            print 'Date of archive ' + stringData

        link = 'http://www.telegraph.co.uk/archive/' + stringData + '.html'
        return link


    def get_all_article_links(self, url, verbose=False):

        # Documentation in BaseCrawler

        links = []
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, from_encoding="utf-8")

        for link in soup.find_all('a', href=True):

            if link['href'].startswith('/finance/'):
                links.append('http://www.telegraph.co.uk' + link['href'])

                # Print links if verbose
                if verbose:
                    print link['href']

                # Add to queue if given
                if self.queue:
                    self.queue.put('http://www.telegraph.co.uk' + link['href'])

        return links

