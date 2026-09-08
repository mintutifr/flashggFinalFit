#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

cats=("tHq_had0_CP_even" "ttH_had0_CP_even" "ttH_had0_CP_odd" "tHq_had0_CP_mix")

# F-test
python3 RunBackgroundScripts.py --inputConfig config_DataCombine.py --mode fTestParallel

# plots
for cat in "${cats[@]}"; do 
    echo ${cat}
    python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root
done



