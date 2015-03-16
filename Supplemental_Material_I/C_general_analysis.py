# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-08 10:02
# modified : 2014-02-08 10:02
"""
Analyze and visualize data for the Analysis

This script replicates the analyses reported in the section "General results"
of the paper.
"""

__author__="Johann-Mattis List"
__date__="2014-02-08"

# switch to xelatex output for networks and set DejaVu Sans as the main font.
import matplotlib as mpl
mpl.use("pgf")
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": [],                   # use latex default serif font
    "font.sans-serif": ["DejaVu Sans"], # use a specific sans-serif font
}
mpl.rcParams.update(pgf_with_rc_fonts)

# set up a latex-preamble
preamble = [r"\usepackage{xltxtra}\usepackage{fontspec}\setmainfont{FreeSans}"]

# define the major reference trees for the analyses
trees = dict(
    arbre = "(Min,((Yue,Hakka),(Wu,(Gan,(Xiang,Mandarin)))));",
    shuxingtu = "((Min,Wu),(Xiang,(Yue,((Hakka,Gan),Mandarin))));",
    southern_chinese = "((Min,Yue,Hakka),(Wu,Gan,Xiang),Mandarin);",
    parsimony = "(Yue,Hakka,Min,(Wu,(Gan,(Xiang,Mandarin))));",
)

# adjust the tree labels with Pinyin symbols
tree_labels = dict(
        Min = "Mǐn",
        Yue = "Yuè",
        Gan = "Gàn",
        Hakka = "Hakka",
        Wu = "Wú",
        Xiang = "Xiāng",
        Mandarin = "Mandarin"
        )

# make major imports
from lingpy import *
from lingpy.compare.phylogeny import PhyBo
from lingpy.convert.plot import *
from lingpy.meaning.basvoc import BasVoc
from sys import argv

# 
if 'tree' in argv:
    for tree in trees:
        plot_tree(
                trees[tree],
                degree=42,
                fileformat="pdf",
                root='root',
                labels=tree_labels,
                filename="plots/tree_"+tree,
                start = 270,
                figsize = (6.5,5.25),
                xliml = -5,
                xlimr = 3,
                ylimt = 6,
                ylimb = 2,
                left = 0.0,
                textsize=18,
                usetex=True,
                change = lambda x:x*6+x**2,
                latex_preamble = preamble
                )

# define the taxon labels
taxa_labels = dict(
        Anyi       = "Ānyì [G]", # 安義
        Beijing    = "Běijīng [MD]",
        Changsha   = "Chángshà [X]",
        Chengdu    = "Chéngdū [MD]",
        Fuzhou     = "Fùzhōu [M]",
        Guangzhou  = "Guǎngzhōu [Y]",
        Lianchang  = "Líanchéng [H]", #连城
        Meixian    = "Měixiàn [H]",
        Nanchang   = "Nánchàng [G]",
        Ningbo     = "Níngbō [W]",
        Ningxia    = "Níngxià [MD]", #宁夏
        Shanghai   = "Shànghǎi (A) [W]",
        Shanghai_B = "Shànghǎi (B) [W]",
        Shuangfeng = "Shuāngfēng [X]",
        Suzhou     = "Sùzhōu [W]",
        Taibei     = "Táiběi [M]",
        Taiyuan    = "Tàiyuán [MD]", # 太原
        Wenzhou    = "Wénzhōu [W]",
        Wuhan      = "Wǔhàn [MD]",
        Xiamen     = "Xiàmén [M]",
        Yingshan   = "Yìngshān [MD]", # 应山
        Yuci       = "Yúcì [MD]", # 榆次
        Zhanping   = "Zhāngpíng [M]", # 漳平
        )

if 'mln' in argv:

    # calculate stats on basic vocabulary
    bv = BasVoc()
    swad = bv.get_list('swadesh100', 'key')
    jach = bv.get_list('jachontov', 'key')
    phy = PhyBo('data/chinese.tsv')
    
    # get number of cognate sets which belong to jach, star, etc.
    jcogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) in jach and \
        phy[k,'pap'] not in phy.singletons]))
    scogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) in swad and \
        phy[k,'pap'] not in phy.singletons and int(phy[k,'swid']) not in jach]))
    rcogs = len(set([phy[k,'proto'] for k in phy if int(phy[k,'swid']) not in swad and \
        phy[k,'pap'] not in phy.singletons and int(phy[k,'swid']) not in jach]))

    # write data to general results
    f = open('results/D_general_results.tsv','w')
    f = open('results/D_specific_results.tsv','w')
    f.close()
    for tree in sorted(trees)+['upgma', 'neighbor_joining', 'random']:
        phy = PhyBo('data/chinese.tsv', tree='trees/'+tree+'.tre', degree=180)
        phy.dataset = '.chinese_'+tree
        phy.filename= '.chinese_'+tree
        phy.analyze(homoplasy=0.05)
        phy.get_MLN(phy.best_model)
        phy.plot_MLN(
                phy.best_model,
                figsize = (14,8.5),
                threshold = 2,
                alphat=True,
                labels = taxa_labels,
                fileformat="pdf",
                filename = 'plots/mln_'+tree,
                cbar_shrink=0.5,
                usetex=True,
                maxweight=12,
                colormap = mpl.cm.binary,
                vedgecolor="black",
                vedgeinnerline=3.0,
                vedgelinewidth=5.0,
                nodestyle='vsd',
                vsd_scale=0.1,
                _prefix = '-- ',
                _suffix = ' --',
                left = 0.05,
                )
        o,p = phy.get_stats(phy.best_model)
        with open('results/C_general_results.tsv', 'a') as f:
            f.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\n'.format(tree, phy.best_model, o, p))

        graph = phy.graph[phy.best_model]
        edges = sorted([e for e in graph.edges(data=True) if 'weight' in e[2]],
                key=lambda x:x[2]['weight'], reverse=True)
        with open('results/C_specific_results.tsv', 'a') as f:
            f.write(tree+'\n-------\n\n')
            jacho,staro,rest = [],[],[]
            for a,b,c in edges:
                f.write('{0} <-> {1} [{2}]\n'.format(a,b,c['weight']))
                f.write(','.join(phy.tree.getNodeMatchingName(a).taxa)+'\n')
                f.write(','.join(phy.tree.getNodeMatchingName(b).taxa)+'\n\n')
                cogs = c['cogs'].split(',')
                for cog in cogs:
                    idx = [x[0] for x in phy.etd[cog] if x != 0][0]
                    proto = phy[idx,'proto']
                    concept = phy[idx,'concept']
                    key = int(phy[idx,'swid'])
                    keyx = ''
                    if key in swad:
                        keyx = '*'
                    if key in jach:
                        keyx = '+'
                    if key in jach:
                        jacho += [proto]
                    elif key in swad:
                        staro += [proto]
                    else:
                        rest += [proto]
                    
                    f.write('{0} "{1}"{2}, '.format(proto,concept,keyx))
                f.write('\n\n')
            j,s,r = len(set(jacho)), len(set(staro)), len(set(rest))
            a = j+s+r
            resu = '{0:.2f}\t{1:.2f}\t{2:.2f}'.format(j/jcogs,s/scogs,r/rcogs)
            print(tree,len(jacho),'\t', len(staro),'\t', len(rest),'\t',resu)


# also write the full trees if this is chosen
if 'full' in argv:
    for tree in ['upgma', 'parsimony', 'neighbor_joining', 'southern_chinese',
            'arbre', 'shuxingtu']:
        print ("plotting {0}".format(tree))
        plot_tree(
                'trees/'+tree+'.tre',
                figsize = (12,8),
                labels = taxa_labels,
                degree = 180,
                filename='plots/reference_'+tree,
                usetex=True,
                fileformat="pdf",
                latex_preamble = preamble
                )

# export data to html
if 'export' in argv:
    wl = Wordlist('wordlists/chinese.tsv')
    wl.export('html', filename='Supplementary_Material_II')
