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
    for l in pmids:
        final.append('+OR+PMID(%s)' % l)
    final.append(end)
    return ''.join(final)

def get_25_citedby(pmids):
    link = create_scopus_link(pmids)
    json = requests.get(link, headers={'X-ELS-APIKEY':API}).json()['search-results']['entry']
    ret = {}
    for pmid, citedby in zip(pmids,json):
        ret[pmid] = int(citedby['citedby-count'])
    return ret

if __name__ == '__main__':
    print(get_citedby(sys.argv[1]))

