# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-07 11:02
# modified : 2015-03-15 13:45
"""
Compare reference trees for performance on ancestral state reconstruction.

This script computes the analyses reported in the "Inferred ancestral states" part of the
paper. It takes to keywords when running it from commandline:

    * TREE [the reference tree which is in the folder trees/, and
    * nobor [boolean flag, specifying whether the analysis should disallow borrowings]
"""

__author__="Johann-Mattis List"
__date__="2015-03-15"

from lingpy import *
from lingpy.compare.phylogeny import *
from sys import argv

# compute the different models
runs = [
        ('weighted',(3,1)),
        ('weighted',(5,2)),
        ('weighted',(2,1)),
        ('weighted',(3,2)),
        ('weighted',(1,1)),
        ]

# change runs to 50:1 in order to disallow for any borrowings
if 'nobor' in argv:
    runs = [('weighted', (50,1))]

# instantiate the wordlist object
phy = PhyBo('data/chinese.tsv', tree='trees/'+argv[1]+'.tre')

# we dot the name of the dataset in order to avoid that our workspace gets
# filled by too many folders containing all the data of the analyses
phy.dataset = ".chinese_"+argv[1]
phy.analyze(runs=runs, plot_dists=True, proto='proto',
        evaluation='average', homoplasy=0.05, gpl=1)

# check for "no-borrowing" specification
if not 'nobor' in argv:
    bm = phy.best_model
else:
    bm = 'w-50-1'

# compute the MLN
phy.get_MLN(bm)

# check how many words in root are also in old chinese, the old roots are
# stored in the file "old_chinese.csv", we label it as "ochW" (Old Chinese,
# Wang Feng), "ach" refers to the words traced by the algorithm back to the
# root
ochW = dict(csv2list('data/old_chinese.csv'))
ach = phy.acs[bm]['root']

# check whether the cognate set is actually in the data
protos = sorted(set([phy[k,'proto'] for k in phy if phy[k,'pap'] not in
    phy.singletons]))

# we now take the words inferred for the root and retrieve them in their
# character spelling
idfdW = [] # means "identifed"
tomuW = [] # stores words which could be retrieved but weren't
for a,b,c in ach:

    # try to get the och entry
    if b in ochW:
        words = ochW[b].split(', ')

        if c in words:
            idfdW += [(b, c, ochW[b])]
        elif [w for w in words if w in protos]:
            tomuW += [(b, c, ochW[b])]

# write results for all detailed hits to the resultsfile
with open('results/D_ancestral_reconstructions_'+argv[1]+'.tsv', 'w') as f:
    f.write('# Incorrectly identified items\n')
    f.write('Concept\tHypothesis\tGold Standard\n')
    for a,b,c in tomuW: f.write(a+'\t'+b+'\t'+c+'\n')
    f.write('\n# Correctly identified items\n')
    f.write('Concept\tHypothesis\tGold Standard\n')
    for a,b,c in idfdW: f.write(a+'\t'+b+'\t'+c+'\n')

# compute the amount of retrieved items
retris = []
for key,val in ochW.items():
    words = val.split(', ')
    if [w for w in words if w in protos]:
        for w in words:
            retris += [(key,w)]

# check for the concepts in order to compute precision and recall, newstuff
# contains all chars reconstructed back to the root
concepts = sorted(set([x[0] for x in retris]))
newstuff = [(line[1],line[2]) for line in ach if line[1] in concepts]

# computed how many words were found and missed
found = len([x for x in retris if x in newstuff])
missed = len([x for x in retris if x not in newstuff])
sold = len([x for x in newstuff if x not in retris])

# calculate test and gold for computation of precision and recall 
test = len(set([x for x in newstuff]))
gold = len(set([x for x in retris]))

# calculate precision, recall, and f-score for the analysis
precision = found / test
recall = found / gold
fscore = 2 * (precision * recall) / (precision + recall)

# print results
print("{0}\t{7}\t{1}\t{2}\t{3}\t{4:.2f}\t{5:.2f}\t{6:.2f}".format(
    argv[1],
    found, 
    len(retris),
    len(newstuff),
    precision,
    recall, fscore, phy.best_model
    ))

# append results to the ancestral_states.tsv-file
with open('results/D_ancestral_states.tsv', 'a') as f:
    if 'nobor' in argv:
        nobor = 1
    else:
        nobor = 0
    f.write(
            '{0}\t{1}\t{2}\t{7}\t{3}\t{4:.2f}\t{5:.2f}\t{6:.2f}\n'.format(
                argv[1],
                'no borrowing  ' if nobor else 'with borrowing',
                found,
                len(newstuff),
                precision, recall, fscore, len(retris)))

