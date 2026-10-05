#!/bin/bash

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0"
    echo
    echo "  Runs makeDatacard.py to build the datacard from the per-category yields"
    echo "  pkl files in yields_tth_th_cp_Analysis/ (produced by ./run_create_yields.sh"
    echo "  - run that first). This is the second half of what used to be"
    echo "  run_create_datacard.sh."
    echo "  -h, --help   Show this help message"
    exit 0
fi

export PYTHONNOUSERSITE=1
source ../setup.sh

# if you are adding new processes, make sure it is also addded to club_workspaces.sh and tool/XSBRMap.py is updated
python3 makeDatacard.py \
    --ext tth_th_cp_Analysis \
    --years 2022preEE,2022postEE,2023preBPix,2023postBPix,2024 \
    --analysis tth_th_cp_Analysis \
    --skipCOWCorr \
    --saveDataFrame \
    --output Datacard_tth_th_cp_Analysis \
    --prune \
    #--doMCStatUncertainty \

# to share the datacard with others, run ./run_move_file_to_eos.sh
