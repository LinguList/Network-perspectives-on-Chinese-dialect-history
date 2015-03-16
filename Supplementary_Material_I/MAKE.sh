python A_analyze_subset.py
sh B_seeding.sh
python C_general_analysis.py full # create reference trees
python C_general_analysis.py mln # create MLNs
python C_general_analysis.py tree # create basic trees of major dialect groups
python C_general_analysis.py export # create supplementary material II (HTML)
sh D_ancestral_state_reconstruction.sh # carry out check for ancestral state reconstruction
