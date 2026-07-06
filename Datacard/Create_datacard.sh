#!/bin/bash

export PYTHONNOUSERSITE=1
source ../setup.sh

PATH_TO_INPUTS=/eos/home-m/mikumar/Final_fits/outputForFinalFits_25June2026/

# years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024")

# for year in "${years[@]}"; do
#     echo "${year}"

#     python3 RunYields.py \
#        --inputWSDirMap  "2022preEE=${PATH_TO_INPUTS}/workspaces/2022preEE/,2022postEE=${PATH_TO_INPUTS}/workspaces/2022postEE/,2023preBPix=${PATH_TO_INPUTS}/workspaces/2023preBPix/,2023postBPix=${PATH_TO_INPUTS}/workspaces/2023postBPix/,2024=${PATH_TO_INPUTS}/workspaces/2024/" \
#         --cats ttH_had0_CP_even,ttH_had0_CP_odd \
#         --procs auto \
#         --ext tth_th_cp_Analysis \
#         --mergeYears \
#         --skipCOWCorr \
#         --batch local
# done

# python3 RunYields.py \
#     --inputWSDirMap  "2022preEE=${PATH_TO_INPUTS}/workspaces/2022preEE/,2022postEE=${PATH_TO_INPUTS}/workspaces/2022postEE/,2023preBPix=${PATH_TO_INPUTS}/workspaces/2023preBPix/,2023postBPix=${PATH_TO_INPUTS}/workspaces/2023postBPix/,2024=${PATH_TO_INPUTS}/workspaces/2024/" \
#     --cats ttH_had0_CP_even,ttH_had0_CP_odd \
#     --procs auto \
#     --ext tth_th_cp_Analysis \
#     --mergeYears \
#     --skipCOWCorr \
#     --batch local

python3 makeDatacard.py \
    --ext tth_th_cp_Analysis \
    --years 2022preEE,2022postEE \
    --analysis tth_th_cp_Analysis \
    --prune --skipCOWCorr \
    --doMCStatUncertainty \
    --saveDataFrame \
    --output Datacard_tth_th_cp_Analysis