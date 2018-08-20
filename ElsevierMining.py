#!/usr/bin/python3
'''
Module for working with elsevier API to mine text of scientific articles.
Requires the the $ELSKEY to be set to the Elsevier API key.
'''
import requests
import string
import pandas as pd
from os import environ

API = environ['ELSKEY']

class Article(object):
    '''
    Class for working with a single article, from id (pii) to clean text
    '''
    
    def __init__(self, link):
        self.link = link
        self.headers = {'X-ELS-APIKey' : API, 'Accept': 'text/plain'}
        
    def get_text(self):
        '''
        Download the text, save it as text and pandas Series
        '''
        self.text = requests.get(self.link, headers=self.headers).text
        self.ser = pd.Series(self.text.split()).str.lower()
        return self.ser
    
    def remove_links(self):
        '''
        Removes links by finding http regex
        '''
        self.ser = self.ser[~self.ser.str.contains('http')]
        return self.ser
    
    def remove_digits(self):
        '''
        Removes the words that contain digits
        '''
        self.ser = self.ser[~self.ser.str.contains('\d')]
        return self.ser
    
    def remove_punctuation(self):
        '''
        Strips all words of punctutation
        '''
        table = str.maketrans('', '', string.punctuation)
        self.ser = self.ser.apply(lambda x: x.translate(table))
        return self.ser
    
    def perform_full(self):
        '''
        Performs the full routine
        '''
        self.get_text()
        self.remove_links()
        self.remove_digits()
        self.remove_punctuation()
        return self.ser

def get_urls(query):
    '''
    Retieves 5000 links that match a certain query using Elsevier API
    '''
    headers = {'X-ELS-APIKey' : API}
    base_link = 'https://api.elsevier.com/content/search/scidir?query=' + query
    ret = []
    for url in requests.get(base_link+'&count=200', headers=headers).json()['search-results']['entry']:
            ret.append(url['prism:url'])
    for n in range(201, 5001, 200):
        for url in requests.get(base_link+'&count=200&start='+str(n), headers=headers).json()['search-results']['entry']:
            ret.append(url['prism:url'])
    return ret

# def get_all_query()


# if __name__ == '__main__':
#     from sys import argv
#     query = argv1[1]
#     get_urls(query)