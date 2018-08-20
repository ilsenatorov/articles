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
    Class for working with a single article
    '''
    
    def __init__(self, link):
        '''
        Creates most vatiables to work with
        '''
        self.link = link
        self.headers_plain = {'X-ELS-APIKey' : API, 'Accept': 'text/plain'}
        self.headers_xml = {'X-ELS-APIKey' : API, 'Accept': 'text/xml'}
        self.xml = requests.get(link, headers=self.headers_xml).text
        self.soup = BeautifulSoup(self.xml, 'xml')
        if self.soup.find('openaccess').get_text() != '0':
            self.open_access = True
            self.text = pd.Series(self.soup.find('sections').get_text(strip=True).split())
            self.abstract = pd.Series(self.soup.find('abstract').get_text(strip=True).split())
        else:
            self.open_access = False
            return


    # def get_text(self):
    #     '''
    #     Gets the actual text of the article
    #     '''
    #     self.text = pd.Series(self.soup.find('sections').get_text(strip=True))

    # def get_clean_text(self):
    #     '''
    #     Returns the text clean
    #     '''
    #     ret = pd.Series(self.get_clean_text().split())
    #     ret = clean_text(ret)
    #     self.clean_abstract = ' '.join(ret.tolist())
    #     return self.clean_text

    def get_scopus(self):
        '''
        Returns the scopus id for the article
        '''
        try:
            self.scopus = self.soup.find('scopus-id').get_text(strip=True)
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
    
    # def get_abstract(self):
    #     '''
    #     Returns the abstract for the article
    #     '''
    #     self.abstract = clean_text(pd.Series(self.soup.find('abstract').get_text(strip=True).tolist()))
    #     return self.abstract
    
    # def get_clean_abstract(self):
    #     '''
    #     Returns the abstract clean 
    #     '''
    #     ret = pd.Series(self.get_clean_abstract().split())
    #     ret = clean_text(ret)
    #     self.clean_abstract = ' '.join(ret.tolist())
    #     return self.clean_abstract
    
    def return_df(self):
        '''
        Returns df row (Series) with all info for the article
        '''
        ret = pd.Series({'link' : self.link,
                        'scopus' : self.get_scopus(),
                        'title' : self.get_title(),
                        'abstract' : clean_text(self.abstract),
                        'text' : clean_text(self.text)})
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
    ser = ser[~ser.str.contains('\d')]
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