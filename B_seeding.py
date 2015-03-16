# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-07 18:09
# modified : 2015-03-16 13:02
"""
Compute seeding analyses and compare how well the algorithm detects the seeds.
"""

__author__="Johann-Mattis List"
__date__="2015-03-16"

from lib.seeding import *
from lingpy import *
from lingpy.compare.phylogeny import *
import os

from sys import argv


runs = 50
tax = 3

if 'one' in argv:
    tax = 3
if 'two' in argv:
    tax = 6
if 'three' in argv:
    tax = 9
if 'four' in argv:
    tax = 12
if 'five' in argv:
    tax = 18

results = []
for i in range(runs):
    wl = Wordlist('data/chinese.tsv')
    seed(wl, ntax=tax)
    
    if argv[1] == 'random':
        os.system('python Z_randomtree.py')

    if 'new' in argv:
        tree = None
        tree_calc = argv[1]
        name = argv[1]+'_new'
    else:
        tree = 'trees/'+argv[1]+'.tre'
        tree_calc = 'upgma'
        name = argv[1]

    phy = PhyBo('data/chinese_seeded.tsv', ref='seedid',
            tree=tree, tree_calc=tree_calc)
    phy.dataset = '.chinese_seeded'
    phy.analyze(homoplasy=0.00)
    phy.get_PDC(phy.best_model, aligned_output=False)
    
    g,m,a,score = evalseed(phy)
    results += [(g,m,a,score)]
    print(i+1,'\t',score, g, m, a)

res = []
for i in range(len(results[0])):
    res += [sum([x[i] for x in results]) / runs]

with open('results/B_seeding_basic'+'_'+str(tax)+'.tsv', 'a') as f:
    f.write('{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\n'.format(name, res[0],
        res[1], res[2], res[3]))
 
 
 
 
 
 
 
 
 
 
 



