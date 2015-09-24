__author__ = 'dominikmajda'

import urllib2

from bs4 import BeautifulSoup
from datetime import timedelta

from source.crawlers.crawler import BaseCrawler, BaseManager


class RoytersCrawler(BaseCrawler):
    """
    Subclass of BaseCrawler for Royters news.
    """

    def dump(self, filename, add_links=False, verbose=False):

        # Documentation in BaseCrawler

        if verbose:
            print "Dumping " + self.url

        # Gather all texts
        content = self.soup.find("span", {"id": "articleText"})

        if not content:
            return False

        # Save to file
        file = open(filename, 'w')

        # Add links if user wants them
        if add_links:
            file.write(self.url + '\n')

        title = self.soup.title.text.lstrip()
        file.write(title.split('|')[0].encode('utf-8') + '\n')
        for tag in content.find_all(text=True):
            if tag.string and tag.string!='\n':
                file.write(tag.string.encode('utf-8'))
                file.write('\n')
        file.close()

        return True

class RoytersManager(BaseManager):

    def get_next_link(self, verbose=False):

        # Get new links if queue is empty
        if self.queue.empty():
            link = self.next_archive_link(verbose)
            links = self.get_all_article_links(link, verbose = False)

            if (verbose):
                print 'Found links: ' + str(len(links))

        return RoytersCrawler(self.queue.get(), self.date)


    def next_archive_link(self, verbose=False):

        # Build new archive link

        self.date = self.date - timedelta(days=1)
        stringData = self.date.strftime('%Y%m%d')

        if(verbose):
            print 'Date of archive ' + stringData

        link = 'http://www.reuters.com/resources/archive/us/' + stringData + '.html'
        return link


    def get_all_article_links(self, url, verbose=False):

        # Documentation in BaseCrawler

        links = []
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, from_encoding="utf-8")

        for link in soup.find_all('a', href=True):

            if link['href'].startswith('http://www.reuters.com/article'):
                links.append(link['href'])

                # Print links if verbose
                if verbose:
                    print link['href']

                # Add to queue if given
                if self.queue:
                    self.queue.put(link['href'])

        return links
