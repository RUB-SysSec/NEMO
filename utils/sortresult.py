#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.7.0, 2019-07-11
:description: Sorts passwords in the strength meter outfile 'eval_result.txt' by likelihood
:usage: pypy utils/sortresult.py results/eval_result.txt > results/eval_result_sorted.txt
'''

import sys

# Read file
with open(sys.argv[1], 'r') as inputfile:
    out = []
    for line in inputfile:
        line = line.rstrip('\r\n')
        splitted = line.split('\t')
        if splitted[0].startswith("Error, no Markov model for this length"):
            out.append((-1.0,splitted[1]))
            # Instead of adding them, you could also discard them
            # pass
        else:
            prob = float(splitted[0])
            pw = splitted[1]
            out.append((prob,pw))

# Sort by prob
out = sorted(out, key=lambda tup: tup[0], reverse=True)

# Output
for entry in out:
    prob = entry[0]
    pw = entry[1]
    print("{}\t{}".format(prob,pw))