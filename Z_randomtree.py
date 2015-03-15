# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-07 12:36
# modified : 2014-02-07 12:36
"""
Create random tree of the data.
"""

__author__="Johann-Mattis List"
__date__="2014-02-07"

from lingpyd import *
from lingpyd.algorithm import squareform
import random

wl = Wordlist('wordlists/chinese.tsv')

D = []
for i,tA in enumerate(wl.taxa):
    for j,tB in enumerate(wl.taxa):
        if i < j:
            d = random.randint(0,100) * 0.01
            D += [d]
D = squareform(D)
tree = upgma(D, wl.taxa, distances=False)

with open('trees/random.tre', 'w') as f:
    f.write(tree)


