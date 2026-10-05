#!/bin/bash

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 [extra args passed through to Plots/makeYieldsTables_tthth.py]"
    echo
    echo "  Runs Plots/makeYieldsTables_tthth.py to build the ttH+tH CP analysis"
    echo "  yields/purity table from Datacard/yields_tth_th_cp_Analysis/."
    echo "  Output: Plots/Tables/yields_table_lite_tthth_tth_th_cp_Analysis.txt"
    echo "  -h, --help   Show this help message"
    exit 0
fi

export PYTHONNOUSERSITE=1
source ../setup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "${SCRIPT_DIR}/../Plots" > /dev/null
python3 makeYieldsTables_tthth.py --ext _tth_th_cp_Analysis "$@"
popd > /dev/null
