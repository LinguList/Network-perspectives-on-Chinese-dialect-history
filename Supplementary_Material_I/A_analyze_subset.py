# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-11 11:37
# modified : 2015-03-11 12:17
"""
Analyze the Subset of the Yinku for illustrational purposes.
"""

__author__="Johann-Mattis List"
__date__="2015-03-11"

# preparations for the use of xelatex along with matplotlib
import matplotlib as mpl
mpl.use("pgf")
pgf_with_rc_fonts = {
    "font.family": "DejaVu Sans",
    "font.serif": [],                   # use latex default serif font
    "font.sans-serif": ["DejaVu Sans"], # use a specific sans-serif font
}
mpl.rcParams.update(pgf_with_rc_fonts)

# import lingpy library
from lingpy import *
from lingpy.compare.phylogeny import *

# set the tree, following roughly the classification proposed by Norman,
# similar to the one used in List et al. 2014
tree='((((((Chengdu,Pingyao),Changsha),Nanchang),(Shanghai,Wenzhou)),(Meixian,Xianggang)),(Fuzhou,Taibei));'

# set up the analysis
phy = PhyBo('data/chinese_subset.tsv', degree=110,tree = tree)
phy.dataset = '.chinese_subset.tsv'

# export distances for the calculation of the neighbor-net analysis
phy.output('dst', filename='results/A_result_subset.dst')

# analyze data within mln approach
phy.analyze(homoplasy=0.0)

# set the taxon labels for nicer formatting with pinyin in output
taxa_labels = dict(
        Beijing    = "Běijīng [MD]",
        Changsha   = "Chángshà [X]",
        Chengdu    = "Chéngdū [MD]",
        Fuzhou     = "Fùzhōu [M]",
        Meixian    = "Měixiàn [H]",
        Nanchang   = "Nánchàng [G]",
        Shanghai   = "Shànghǎi [W]",
        Taibei     = "Táiběi [M]",
        Wenzhou    = "Wénzhōu [W]",
        Xiamen     = "Xiàmén [M]",
        Xianggang  = 'Hongkong [Y]',
        Pingyao    = 'Píngyáo [MD]',
        )

phy.plot_MLN(phy.best_model, filename='plots/A_chinese_subset', labels=taxa_labels,
        fileformat='pdf', colormap=mpl.cm.binary, nodestyle='vsd',
        linescale=0.75)

# note that the final plot was later edited with help of InkScape SVG editor in
# order to enhance visibility
