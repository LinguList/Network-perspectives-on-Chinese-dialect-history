# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-08 12:33
# modified : 2014-02-08 12:33
"""
Calculate random phylogenies and store percentages.
"""

__author__="Johann-Mattis List"
__date__="2014-02-08"

from lingpy.compare.phylogeny import *
from lingpy.meaning.basvoc import *
import os

# calculate stats on basic vocabulary
bv = BasVoc()
swad = bv.get_list('swadesh100', 'key')
jach = bv.get_list('jachontov', 'key')
phy = PhyBo('wordlists/chinese.tsv')

# get number of cognate sets which belong to jach, star, etc.
jcogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) in jach and \
    phy[k,'pap'] not in phy.singletons]))
scogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) in swad and \
    phy[k,'pap'] not in phy.singletons and int(phy[k,'swid']) not in jach]))
rcogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) not in swad and \
    phy[k,'pap'] not in phy.singletons and int(phy[k,'swid']) not in jach]))

results = []
for i in range(50):
    
    os.system('python Z_randomtree.py')
    phy = PhyBo('wordlists/chinese.tsv', tree="trees/random.tre",
            homoplasy=0.00)
    phy.dataset = '.random'
    phy.analyze()
    n,p = phy.get_stats(phy.best_model)

    # get subsets
    phy.get_MLN(phy.best_model)
    graph = phy.graph[phy.best_model]
    edges = sorted([e for e in graph.edges(data=True) if 'weight' in e[2]],
            key=lambda x:x[2]['weight'], reverse=True)
    jacho, staro, rest = [],[],[]
    for a,b,c in edges:
        cogs = c['cogs'].split(',')
        for cog in cogs:
            idx = [x[0] for x in phy.etd[cog] if x != 0][0]
            proto = phy[idx,'proto']
            concept = phy[idx,'concept']
            key = phy[idx,'swid']
            if key in jach:
                jacho += [proto]
            elif key in swad:
                staro += [proto]
            else:
                rest += [proto]
    j,s,r = len(set(jacho)), len(set(staro)), len(set(rest))

    
    print('{0}\t{1}\t{2}'.format(phy.best_model, n, p))
    results += [(phy.best_model, n, p, j/jcogs, s/scogs, r/rcogs)]

with open('A_general_specific_results_random', 'w') as f:

    N = sum([l[1] for l in results]) / 50
    P = sum([l[2] for l in results]) / 50
    J = sum([l[3] for l in results]) / 50
    S = sum([l[4] for l in results]) / 50
    R = sum([l[5] for l in results]) / 50
 
    
    modls = [l[0] for l in results]
    M = sorted(modls, key=lambda x: modls.count(x), reverse=True)[0]

    f.write('{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}'.format(M,N,P,J,S,R))
    

