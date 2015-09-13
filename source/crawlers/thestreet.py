__author__ = 'dominikmajda'
import urllib2
import re

from bs4 import BeautifulSoup
from datetime import datetime

from source.crawlers.crawler import BaseCrawler, BaseManager


class TheStreetCrawler(BaseCrawler):
    """
    Subclass of BaseCrawler for ZeroHedge news.
    """

    def __init__(self, url, date):
        BaseCrawler.__init__(self, url, date)

        # This crap repairs this site divs
        self.html = self.html.replace('<hr align="CENTER" noshade="noshade" width="150" />',
                                      '<hr align="CENTER" noshade="noshade" width="150">')
        self.html = self.html.replace('<div id="premiumTextAd">', '</hr><div id="premiumTextAd">')
        self.soup = BeautifulSoup(self.html, from_encoding="utf-8")

    def dump(self, filename, add_links=False, verbose=False):

        # Documentation in BaseCrawler

        if verbose:
            print "Dumping " + self.url

        # kill all script and style elements
        for script in self.soup(["script", "style"]):
            script.extract()    # rip it out

        # Gather all texts
        content = self.soup.find_all("div", {"id":"storyBody"})

        if not content:
            return False

        # Save to file
        file = open(filename, 'w')

        # Add links if user wants them
        if add_links:
            file.write(self.url + '\n')

        title = self.soup.title.text.lstrip().encode('utf-8')
        file.write(title.replace(' - TheStreet', '\n'))

        for tag in content[0].find_all("p"):
            if tag.text and tag.text!='\n':
                file.write(tag.text.replace('\n','').encode('utf-8'))
                file.write('\n')

        # Rest of the text
        rest = self.soup.find_all("hr", {"align":"CENTER"})
        if (rest and len(rest)>1):
            soup = BeautifulSoup(rest[1].get_text())
            if (len(soup.find_all(text=True))>0):
                text = soup.find_all(text=True)[0]
                text =re.sub(r'Must Read:.*', r'', text)
                file.write(text.encode('utf-8'))

        file.close()

        return True


class TheStreetManager(BaseManager):

    def __init__(self, date = datetime.now(), page = 0):
        BaseManager.__init__(self, date)
        self.page = page


    def get_next_link(self, verbose=False):

        # Get new links if queue is empty
        if self.queue.empty():
            link = self.next_archive_link(verbose)
            links = self.get_all_article_links(link, verbose = False)

            if (verbose):
                print 'Found links: ' + str(len(links))

        return TheStreetCrawler(self.queue.get(), self.date)

    def next_archive_link(self, verbose=False):

        # Build new archive link

        if(verbose):
            print 'Page of archive ' + str(self.page)

        link = 'http://www.thestreet.com/headlines-and-perspectives/financial-services/more.html?currentPageNumber='\
               + str(self.page) +'&perPage=100'

        # Increase page of archive
        self.page += 1

        return link



    def get_all_article_links(self, url, verbose=False):

        # Documentation in BaseCrawler

        links = []
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, from_encoding="utf-8")

        for link in soup.find_all('a', href=True):

            if link['href'].startswith('/story/') and link.parent['class'][0]=="headline":

                links.append('http://www.thestreet.com' + link['href'])

                # Print links if verbose
                if verbose:
                    print link['href']

                # Add to queue if given
                if self.queue:
                    self.queue.put('http://www.thestreet.com' + link['href'])

        return links

