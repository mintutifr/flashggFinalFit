#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

# If edit the categories here then edit the categoried in `config_DataCombine.py` as well
cats=( "ttH_had0_CP_even" "ttH_had0_CP_odd") # "tHq_had0_CP_mix" "tHq_had0_CP_even")

# F-test
# output stored in `outdir_tth_th_cp_Analysis/`
python3 RunBackgroundScripts.py --inputConfig config_DataCombine.py --mode fTestParallel

# plots
for cat in "${cats[@]}"; do 
    echo ${cat}
    python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root
done



