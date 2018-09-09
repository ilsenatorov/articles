#!/usr/bin/python3
import mining
pmids = open('pmids.tsv').read().split('\n')
for num in range(25, len(pmids), 25):
    cit25 = mining.get_25_citedby(pmids[num-25:num])
    with open('citations.tsv', 'a+') as output:
        for cit in cit25:
            output.write(str(cit) + '\t' + str(cit25[cit])+'\n')