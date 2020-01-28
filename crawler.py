# standard libs
import json
import sys
import hashlib
import requests
from bs4 import BeautifulSoup
import threading
import re

# has list of links and scraping methods for pages / domains
class crawler():

    isAddress = r'https://www.foxnews.com'

    #  get the links on the domain's main page
    def __init__(self, domain):
        self.domain = domain
        self.toSearch = set()
        self.searched = set()
        while len(self.searched) < 500:
            self.scrapePage(self.domain)
            self.searchLinks()

    # appends all new links to self.links
    def scrapePage(self, address):
        links = []
        r = requests.get(address)
        print('QUERIED {}'.format(address))
        soup = BeautifulSoup(r.text, 'html.parser')
        theList = soup.find_all('a', href=True)
        for ref in theList:
            link = ref['href']
            if re.match(self.isAddress, link):
                if link not in self.searched:
                    if link not in self.toSearch:
                        self.toSearch.add(ref['href'])

    # thread the exploration of the generated set of links
    def searchLinks(self):
        self.searched |= self.toSearch
        if len(self.toSearch) > 0:
            if len(self.toSearch) > 100:
                print("NUMBER OF THREADS:\t\t100")
                threads = [threading.Thread(target=self.scrapePage, args=(link,)) for link in self.toSearch[:100]]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                self.toSearch = {}
            else:
                print("NUMBER OF THREADS:\t\t{}".format(len(self.toSearch)))
                threads = [threading.Thread(target=self.scrapePage, args=(link,)) for link in self.toSearch]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                self.toSearch = set()

        else:
            print('PASSED')

        self.fileWrite()


    # write all of the links to text file; deleting file will rebuild
    def fileWrite(self):
        with open('hrefs.txt', 'a') as f:
            for link in self.searched:
                f.write(link + '\n')
            f.close()

if __name__ == '__main__':

    c = crawler(sys.argv[1])
    c.fileWrite()
