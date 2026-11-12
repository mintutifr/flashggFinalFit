#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

# If edit the categories here then edit the categoried in `config_DataCombine.py` as well
cats=("ttH_had0_CP_even" "ttH_had0_CP_odd" "ttH_had0_CP_mix" \
      "ttH_had1_CP_even" "ttH_had1_CP_odd" "ttH_had1_CP_mix" \
      "ttH_lep0_CP_even" "ttH_lep0_CP_odd" "ttH_lep0_CP_mix" \
      "ttH_lep1_CP_even" "ttH_lep1_CP_odd" "ttH_lep1_CP_mix" \
      "tHq_had0_CP_even" "tHq_had0_CP_odd" "tHq_had0_CP_mix" \
      "tHq_had1_CP_even" "tHq_had1_CP_odd" "tHq_had1_CP_mix" \
      "tHq_lep0_CP_even" "tHq_lep0_CP_odd" "tHq_lep0_CP_mix" \
      "tHq_lep1_CP_even" "tHq_lep1_CP_odd" "tHq_lep1_CP_mix")

# F-test
# output stored in `outdir_tth_th_cp_Analysis/`
python3 RunBackgroundScripts.py \
    --inputConfig config_DataCombine.py \
    --mode fTestParallel \
    --printOnly

ls outdir_tth_th_cp_Analysis/fTestParallel/jobs/sub_fTestParallel_tth_th_cp_Analysis_*.sh \
    | xargs -P 8 -I{} bash {}

# plots
for cat in "${cats[@]}"; do 
    echo ${cat}
    python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root
done



