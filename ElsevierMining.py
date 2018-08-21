#!/usr/bin/python3
'''
Module for working with elsevier API to mine text of scientific articles.
Requires the the $ELSKEY to be set to the Elsevier API key.
'''
import requests
import string
import pandas as pd
import os
from bs4 import BeautifulSoup
import numpy as np

API = os.environ['ELSKEY']

class Article(object):
    '''
    Class for working with a single article. 
    Requires the API link to work, usually fetched throug get_urls function
    '''
    
    def __init__(self, link):
        '''
        Creates most vatiables to work with
        '''
        self.link = link
        self.headers = {'X-ELS-APIKey' : API}
        self.headers_plain = {'X-ELS-APIKey' : API, 'Accept': 'text/plain'}
        self.headers_xml = {'X-ELS-APIKey' : API, 'Accept': 'text/xml'}
        self.xml = requests.get(link, headers=self.headers_xml).text
        self.soup = BeautifulSoup(self.xml, 'xml')
        if self.soup.find('openaccess').get_text() != '0':
            self.open_access = True
        else:
            self.open_access = False
            return


    def get_text(self):
        try:
            self.text = pd.Series(self.soup.find('sections').get_text(strip=True).split())
            return self.text
        except:
            self.text = np.nan
            return self.text
    
    def get_abstract(self):
        try:
            self.abstract = pd.Series(self.soup.find('abstract').get_text(strip=True).split())
            return self.abstract
        except:
            self.abstract = np.nan
            return self.abstract


    def get_scopus(self):
        '''
        Returns the scopus id for the article
        '''
        try:
            self.scopus = int(self.soup.find('scopus-id').get_text(strip=True))
            return self.scopus
        except:
            self.scopus = np.nan
            return np.nan

    def get_title(self):
        '''
        Returns the title for the article
        '''
        try:
            self.title = self.soup.find('title').get_text(strip=True)
            return self.title
        except:
            self.title = np.nan
            return np.nan
    
    def get_cited_by(self):
        '''
        Gets number of citations. Requires the self.scopus variable, self.get_scopus needs to be run first
        '''
        try:
            r = requests.get('http://api.elsevier.com/content/search/scopus?query=SCOPUS-ID(%d)&field=citedby-count' % self.scopus, headers=self.headers)
            return int(r.json()['search-results']['entry'][0]['citedby-count'])
        except:
            return np.nan
    
    def return_df(self):
        '''
        Returns df row (Series) with all info for the article
        '''
        ret = pd.Series({'link' : self.link,
                        'scopus' : self.get_scopus(),
                        'title' : self.get_title(),
                        'abstract' : clean_text(self.get_abstract()),
                        'text' : clean_text(self.get_text()),
                        'citations' : self.get_cited_by()})
        return ret


def remove_links(ser):
    '''
    Removes links by finding http regex
    '''
    ser = ser[~ser.str.contains('http')]
    return ser
    
def remove_digits(ser):
    '''
    Removes the words that contain digits
    '''
    ser = ser[~ser.str.contains(r'\d')]
    return ser

def remove_punctuation(ser):
    '''
    Strips all words of punctutation
    '''
    table = str.maketrans('', '', string.punctuation)
    ser = ser.apply(lambda x: x.translate(table))
    return ser

def clean_text(ser):
    '''
    Cleans the text completely
    '''
    ret = remove_links(ser)
    ret = remove_digits(ret)
    ret = remove_punctuation(ret)
    return ret


def get_urls(query, number=5001):
    '''
    Retieves 5000 links that match a certain query using Elsevier API
    '''
    headers = {'X-ELS-APIKey' : API}
    base_link = 'https://api.elsevier.com/content/search/scidir?query=' + query
    ret = []
    for url in requests.get(base_link+'&count=200', headers=headers).json()['search-results']['entry']:
            ret.append(url['prism:url'])
    for n in range(201, number, 200):
        for url in requests.get(base_link+'&count=200&start='+str(n), headers=headers).json()['search-results']['entry']:
            ret.append(url['prism:url'])
    return ret

def run_routine(query, number=5000):
    '''
    Run the whole routine for one query.
    '''
    df = pd.DataFrame(columns=['link', 'scopus', 'title', 'abstract', 'text', 'citations'])
    n=0
    for link in get_urls(query, number=number):
        try:
            A = Article(link)
            if A.open_access:
                df.loc[n] = Article(link).return_df()
                n+=1
            else:
                print('article is not open access, skipping')
        except:
            print('Failed to retrieve info')
    return df

if __name__ == '__main__':
    '''
    Using the module as the function, returns a tsv file
    '''
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-q", help="query to search for", type=str)
    parser.add_argument("-n", help="number of articles to save", type=int)
    args = parser.parse_args()
    run_routine(args.q, number=args.n).to_csv('./%s_%d.tsv' % (args.q, args.n), sep='\t')
