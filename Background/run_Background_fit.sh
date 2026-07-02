#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

# F-test
# python3 RunBackgroundScripts.py --inputConfig config_DataCombine.py --mode fTestParallel

# plots
# for cat in ttH_had0_CP_even ttH_had0_CP_mix ttH_had0_CP_odd ttH_had1_CP_even ttH_had1_CP_mix ttH_had1_CP_odd ; do python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root; done
# for cat in ttH_lep0_CP_even ttH_lep0_CP_mix ttH_lep0_CP_odd ttH_lep1_CP_even ttH_lep1_CP_mix ttH_lep1_CP_odd ; do python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root; done

# for cat in ttH_had0_CP_even ttH_had0_CP_odd ; do python3 ../Plots/makeMultipdfPlot.py --inputWSFile ../Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_${cat}.root --cat ${cat} --ext tth_th_cp_Analysis --mass 125 --inputSignalWSFile ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_${cat}.root; done


