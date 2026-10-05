#!/bin/bash

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0"
    echo
    echo "  Runs RunYields.py for every (year, category) to (re)build the per-category"
    echo "  yields pkl files in yields_tth_th_cp_Analysis/. This is the first half of"
    echo "  what used to be run_create_datacard.sh - split out because everything that"
    echo "  reads yields_tth_th_cp_Analysis/*.pkl (run_makeYieldsTables_tthth.sh,"
    echo "  run_count_mc_events.sh, run_makeEventTables_tthth.sh) only depends on this"
    echo "  step, not on run_build_datacard.sh (makeDatacard.py, incl. --prune)."
    echo "  -h, --help   Show this help message"
    exit 0
fi

export PYTHONNOUSERSITE=1
source ../setup.sh

PATH_TO_INPUTS=/eos/home-m/mikumar/Final_fits/outputForFinalFits_7Sep2026/

years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024")
cats=("ttH_had0_CP_even" "ttH_had0_CP_odd") # "tHq_had0_CP_even"  "tHq_had0_CP_mix")

for year in "${years[@]}"; do
    echo "${year}"
    for cat in "${cats[@]}"; do
        echo "${cat}"
        python3 RunYields.py \
        --inputWSDirMap  "2022preEE=${PATH_TO_INPUTS}/workspaces/2022preEE/,2022postEE=${PATH_TO_INPUTS}/workspaces/2022postEE/,2023preBPix=${PATH_TO_INPUTS}/workspaces/2023preBPix/,2023postBPix=${PATH_TO_INPUTS}/workspaces/2023postBPix/,2024=${PATH_TO_INPUTS}/workspaces/2024/" \
            --cats ${cat} \
            --procs 'GG2H,TTH,tHqHad,tHqHadCPodd,tHqLep,tHqLepCPodd,tthCPodd' \
            --ext tth_th_cp_Analysis \
            --mergeYears \
            --skipCOWCorr \
            --batch local
    done
done

