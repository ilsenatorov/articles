#!/usr/bin/python3
import mining
pmids = open('pmids.tsv').read().split('\n')
for num in range(25, len(pmids), 25):
    mining.get_25_citedby(pmids[num-25:num])
    