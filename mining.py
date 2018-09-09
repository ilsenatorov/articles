#!/usr/bin/python3
import pandas as pd
import numpy as np
import requests
import os
import sys

API = os.environ['ELSKEY']


def get_citedby(PMID):
    try: 
        scopus = requests.get('http://api.elsevier.com/content/search/scopus?query=PMID(%s)&field=citedby-count' % PMID, headers={'X-ELS-APIKEY':API})
        return scopus.json()['search-results']['entry'][0]['citedby-count']
    except Exception as e:
        print(e)
        return np.nan

def create_scopus_link(pmids):
    beg = 'http://api.elsevier.com/content/search/scopus?query=PMID(%s)' % pmids[0]
    final = [beg]
    end = '&field=citedby-count'
    for l in pmids[1:]:
        final.append('+OR+PMID(%s)' % l)
    return ''.join(final)

def get_25_citedby(pmids):
    link = create_scopus_link(pmids)
    json = requests.get(link, headers={'X-ELS-APIKEY':API}).json()['search-results']['entry']
    for pmid, info in zip(pmids,json):
        try:
            date = info['prism:coverDate']
            citedby = info['citedby-count']
            title = info['dc:title']
            pubmed = info['pubmed-id']
            with open('citations.tsv', 'a+') as output:
                output.write('%s\t%s\t%s\t%s\t%s\n' % (pmid, date, citedby, title, pubmed))
        except:
            print('Unable to retrieve article with PMID %s' % pmid)

if __name__ == '__main__':
    print(get_citedby(sys.argv[1]))

