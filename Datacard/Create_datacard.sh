#!/bin/bash

export PYTHONNOUSERSITE=1
source ../setup.sh

# PATH_TO_INPUTS=/eos/home-m/mikumar/Final_fits/outputForFinalFits_25June2026/

# python3 RunYields.py \
#     --inputWSDirMap 2022preEE=$PATH_TO_INPUTS/workspaces/2022preEE/ \
#     --cats ttH_had0_CP_even,ttH_had0_CP_odd \
#     --procs auto \
#     --ext tth_th_cp_Analysis_2022preEE \
#     --mergeYears \
#     --skipCOWCorr  \
#     --batch local \

python3 makeDatacard.py --ext tth_th_cp_Analysis_2022preEE --years 2022preEE --analysis tth_th_cp_Analysis --prune --skipCOWCorr --doMCStatUncertainty --saveDataFrame --output Datacard_tth_th_cp_Analysis