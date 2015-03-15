# Supplementary Material I: The code basis

This is the code that replicates all analyses presented in the paper. It consists of four parts:

A: A subset-analysis of the MLN which also outputs a distance matrix of the subset which can then be imported in SplitsTree and analysed using methods like Neighbor-Net or SplitDecomposition.
B: The seeding analysis in which fake-borrowings are produced and the algorithm then checks how well the MLN method retrieves these fake borrowings.
C: The general analysis whose results are reported in the Paragraph 3.3.1 of the paper.
D: The specific analysis regardng ancestral state reconstruction whose results are reported in Paragraph 3.3.2 of the paper.

Running the analysis requires specific parameters to be passed to the various scripts. In order to check which parameters are needed or to run all analyses at once (this will take some time, since the random analyses are all repeated), just open a terminal on a Unix machine and type:

$ sh MAKE.sh

Alternatively, you can run parts of the analysis. Look at the commands which are used in the MAKE.sh file in order to see which arguments need to be provided. As a general rule: All shell files run without parameters, so you might just want to try these.

Note that this code requires certain dependencies to work. You will need:

1. LingPy, Version 2.3 or higher (http://lingpy.org)
2. The dependencies that LingPy needs (see at http://lingpy.org), including MatplotLib (a python library for plotting) and networkx (a Python library for network approaches).
3. XeTeX for all plots to work properly.

If there are questions on how to use this code or you detect bugs, please don't hesitate to contact me at <mattis.list@lingpy.org>.
