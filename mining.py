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

if __name__ == '__main__':
    print(get_citedby(sys.argv[1]))