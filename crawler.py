# standard libs
import json
import sys
import hashlib

# installed libs
import requests
from bs4 import BeautifulSoup

# has list of links and scraping methods for pages / domains
class crawler():

    #  get the links on the domain's main page
    def __init__(self, domain):
        self.domain = domain
        self.links = []
        self.scrapePage(self.domain)

    # appends all new links to self.links
    def scrapePage(self, address):
        r = requests.get(address)
        soup = BeautifulSoup(r.text, 'html.parser')
        theList = soup.find_all('a', href=True)
        for ref in theList:
            if ref['href'] not in self.links:
                self.links.append(ref['href'])

    # hash all of the links to make sure there aren't repeats
    def makeHash(self, input):
        m = hashlib.md5()
        m.update(input)
        m.digets()
        return(m)

    # write all of the links to text file; deleting file will rebuild
    def fileWrite(self):
        with open('hrefs.txt', 'a') as f:
            for link in self.links:
                f.write(link + '\n')

if __name__ == '__main__':

    c = crawler(sys.argv[1])
    c.fileWrite()
