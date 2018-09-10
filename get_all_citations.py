#!/usr/bin/python3
'''
Main functon that writes down metadata for articles.
'''
import mining
pmids = open('pmids.tsv').read().split()
for num in range(25, len(pmids), 25):
    mining.get_25_citedby(pmids[num-25:num], './citations.tsv')
    