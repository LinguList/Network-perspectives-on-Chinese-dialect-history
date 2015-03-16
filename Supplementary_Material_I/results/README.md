# Results for the Analyses

Once you run the analyses in this repository successfully, a couple of results will be produced. The formats are basically all given in simple TSV files and should be easy to understand. However, in order to facilitate the process of reading the results, a short summary is given in the following.

# Type-A Results

Analysis A gives the results for the small study on just a subset of languages based on the primary data that was used in the study of [List et al. (2014)](http://bibliography.lingpy.org?key=List2014b) and is based on the data set of [Hóu (2004)](http://bibliography.lingpy.org?key=Hou2004). 

When running the analyses, the folder plots/ will produce a plot of the minimal lateral network, called `A_chinese_subset.pdf`. It further produces an output file in the results folder, called `A_result_subset.dst`. This file contains the distance matrix which can further be passed to software packages like SplitsTree in order to visualize the data with help of [NeighborNet](http://bibliography.lingpy.org?key=Bryant2002) (as done in the paper).

# Type-B Results

These are the results of the "seeding" analysis in which fake borrowings were produced in the original dataset used in [Ben Hamed and Wang (2006)](http://bibliography.lingpy.org?key=Hamed2006). Producing the results will take a considerable amount of time, since for each reference tree and each seeding degree (3, 6, 9, 12, 18), the analysis is repeated 50 times as a default and the results are averaged in the end. If you run all analyses, this will produce 5 differen files, each called `B_seeding_basic_TAXLEN.tsv`, with TAXLEN being the number of "infected" languages/dialects in the analyses (3, 6, 9, etc.). The files are tab-separated and indicate how well the algorithm labelled borrowed items as such. The first column shows the reference tree which was used, and the following three columns indicate the number of detected borrowings, the number of missed borrowings, and the general number of borrowings, on average. The last column indicates the ratio of detected borrowings and the total amount of seeded borrowings. 

# Type-C Results

The results in part C of this repository show the general results of MLN analyses along with MLN plots and a calculation of sublist percentages (how many "borrowed" words belong to Jachontov's sublist, how many to Swadesh's list of 100 items, etc.). In the results/ folder, you will find these results encoded in two files:

* `C_general_results.tsv`, showing the name of the reference tree, the optimal model (gain-loss ratio), the average number of origins on the reference tree, and the average number of "patchy" cognate sets.
* `C_specific_results.tsv`, showing in detail for each of the reference trees, which lateral edges have been in ferred, and which items make up for the matches, and between wich languages and ancestral languages the edges are inferred. The format here starts by listing the name of the reference tree, then follows an empty line, then follows the edge with abbreviated names for internal nodes and the number of inferred patchy links indicated in squared brackets (like "Xiamen <-> edge.19 [4]"). The next two lines indicate the descendant languages of the two nodes (if the actual node is a leaf node, it has itself as a descendant). After another blank line, the basic vocabulary items are listed both with their Chinese character (representing the cognate set) and their meaning. An asterisk here indicates that the concept belongs to Jachontov's list, and a plus indicates that it belongs to Swadesh's list of 100 items.

If you run the full analysis for type C with help of the shell script. The analyses further produces plots of minimal lateral networks, given in the plots/ folder, and labelled as `mln_REF.pdf`, where REF is replaced by the name of the reference tree. It also produces all reference trees in "isolation", labelled as `reference_REF.pdf`, and small reference trees in which only the major dialect groups occur as leaves.

# Type-D Results

These results show the estimation of the quality of ancestral-state reconstruction as carried out by the MLN approach. It produces three files showing the detailed account of ancestral states reconstructed for each reference tree, which are named as `D_ancestral_reconstructions_REF.tsv` and indicate incorrectly identifed and correctly identified items in three columns, the first showing the concept, the second the result of the automatic analysis, and the third the "Gold Standard" which is the Old Chinese word (character) as proposed in the original data used in [Ben Hamed and Wang 2006](http://bibliography.lingpy.org?key=Hamed2006). A further file, named `D_ancestral_states.tsv` lists the aggregated results in TSV-format with the first column indicating the name of the reference tree, the second indicating whether borrowing was allowed or not, the third to fifth column listing the number of correctly inferred ancestral states, the number of inferrable ancestral states, and the number of proposed ancestral states. The last three columns list the values for precision, recall, and f-scores (harmonic mean). 


