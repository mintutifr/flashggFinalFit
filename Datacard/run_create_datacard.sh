#!/bin/bash

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0"
    echo
    echo "  Runs RunYields.py + makeDatacard.py to (re)build the datacard."
    echo "  -h, --help   Show this help message"
    exit 0
fi

export PYTHONNOUSERSITE=1
source ../setup.sh

PATH_TO_INPUTS=/eos/home-m/mikumar/Final_fits/outputForFinalFits_7Sep2026/

years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024")
cats=("tHq_had0_CP_even" "ttH_had0_CP_even" "ttH_had0_CP_odd" "tHq_had0_CP_mix")

for year in "${years[@]}"; do
    echo "${year}"
    for cat in "${cats[@]}"; do
        echo "${cat}"
        python3 RunYields.py \
        --inputWSDirMap  "2022preEE=${PATH_TO_INPUTS}/workspaces/2022preEE/,2022postEE=${PATH_TO_INPUTS}/workspaces/2022postEE/,2023preBPix=${PATH_TO_INPUTS}/workspaces/2023preBPix/,2023postBPix=${PATH_TO_INPUTS}/workspaces/2023postBPix/,2024=${PATH_TO_INPUTS}/workspaces/2024/" \
            --cats ${cat} \
            --procs auto \
            --ext tth_th_cp_Analysis \
            --mergeYears \
            --skipCOWCorr \
            --batch local
    done
done

# if you are adding new processes, make sure it is also addded to club_workspaces.sh and tool/XSBRMap.py is updated
python3 makeDatacard.py \
    --ext tth_th_cp_Analysis \
    --years 2022preEE,2022postEE,2023preBPix,2023postBPix,2024 \
    --analysis tth_th_cp_Analysis \
    --prune --skipCOWCorr \
    --doMCStatUncertainty \
    --saveDataFrame \
    --output Datacard_tth_th_cp_Analysis

# to share the datacard with others, run ./run_move_file_to_eos.sh
