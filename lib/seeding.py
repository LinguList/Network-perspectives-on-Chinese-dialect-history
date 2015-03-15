# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-01-14 16:37
# modified : 2015-03-15 16:00
"""
Create artificial seeds of fake borrowings for testing purposes.
"""

__author__="Johann-Mattis List"
__date__="2015-03-15"

from lingpy import *
import random
from sys import argv

def seed(wl, target="seedid", ntax=3, mode="simple", degree=0.25):
    """
    * ntax : number of taxa to be infected
    * target : name of target identifier
    * mode : we could think of different models, here, we create a simple
      source-target model in which one language pair is determined first, and
      later on this language pair exchanges cognates as borrowings
    * degree : determine the amount of words that should be exchanged as
      borrowings
    """
    
    if mode == 'simple':
        
        sources = []
        targets = []

        numbers = list(range(wl.width))

        for n in range(ntax):
            
            s = random.choice(numbers)
            #del numbers[numbers.index(s)]
            
            while True:
                t = random.choice(numbers)
                if t != s:
                    break
            #del numbers[numbers.index(t)]

            sources += [wl.taxa[s]]
            targets += [wl.taxa[t]]
        
        # create dictionary for cognate ids
        d1 = dict([(key,wl[key,'cogid']) for key in wl])
        d2 = dict([(key,0) for key in wl])
        
        for s,t in zip(sources, targets):
            
            # get cogids for first language
            cogS = wl.get_dict(language=s, flat=True)
            cogT = wl.get_dict(language=t, entry='cogid', flat=True)
            
            nums = int(len(cogT) * degree)

            concepts = random.sample(wl.concepts, nums)

            for c in concepts:
                if c in cogS and c in cogT:
                    # get cognate id for seed
                    cid = cogT[c][0]

                    # now add this to dictionary for transformation
                    tid = cogS[c][0]
                    if wl[tid,'cogid'] != cid:
                        d1[tid] = cid
                        d2[tid] = 1
        
        wl.add_entries(target, d1, lambda x:x)
        wl.add_entries('loan', d2, lambda x:x) 
        wl._meta['seeds'] = [','.join(sources), ','.join(targets)]
        try:
            del wl._meta['taxa']
            del wl._meta['doculect']
        except:
            pass

        wl.output('tsv', filename=wl.filename.replace('.tsv','')+'_seeded', ignore=["taxa"])
    

def evalseed(wl):
    """
    Evaluate accuracy of an actual seeding analysis.
    """
    
    goods, alls, missed = 0,0,0

    for key in wl:
        l = wl[key,'loan']
        p = wl[key,'patchy']
         

        if l == "1": 
            if not p.endswith('0'):
                goods += 1
            else:
                missed += 1
            alls += 1
    return goods, missed, alls, goods / alls

if __name__ == '__main__':
    wl = Wordlist(argv[1]+'.qlc')
    seed(wl)
    

    from lingpyd.compare.phylogeny import PhyBo

    #bor2 = PhyBo(argv[1]+'.qlc', ref="cogid")
    #bor2.analyze()
    #bor2.get_MLN(bor2.best_model)
    #bor2.plot_MLN(bor2.best_model)

    if 'neighbor' in argv:
        borX = Wordlist(argv[1]+'_seeded.qlc')
        try:
            del borX._meta['tree']
        except:
            pass
        borX.calculate('tree', method='neighbor',ref="cogid")
        borX.output('qlc', filename=argv[1]+'_seeded')

    if 'upgma' in argv:
        borX = Wordlist(argv[1]+'_seeded.qlc')
        try:
            del borX._meta['tree']
        except:
            pass
        borX.calculate('tree', method='upgma', ref="cogid")
        borX.output('qlc', filename=argv[1]+'_seeded')


    bor1 = PhyBo(argv[1]+'_seeded.qlc', ref="seedid")
    bor1.analyze(mixed=False)
    bor1.get_MLN(bor1.best_model)
    bor1.plot_MLN(bor1.best_model)
    bor1.get_PDC(bor1.best_model, aligned_output=False)
    goods = 0
    missed = 0
    alls = 0

    for key in bor1:
        l = bor1[key,'loan']
        p = bor1[key,'patchy']
        

        if l == "1": 
            if not p.endswith('0'):
                goods += 1
            else:
                missed += 1
            alls += 1
    
    print(goods,missed, alls, '{0:.2f}'.format(goods / alls))
    




