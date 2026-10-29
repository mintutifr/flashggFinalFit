#!/bin/bash

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0"
    echo
    echo "  Runs txt to workspace and combine to perform the fit"
    echo "  -h, --help   Show this help message"
    exit 0
fi

export PYTHONNOUSERSITE=1
source ../setup.sh

# create workspace using the datacard txt files (datacard + Models/ shapes read from indir, output written here)
echo
echo "  Creating workspace from datacard txt files..."
python3 RunText2Workspace.py --mode cpTopHiggs  --POI doFCPOI --batch local --ext _tth_th_cp_Analysis \
        --indir /eos/home-m/mikumar/php-plots/tth_analysis/Final_fits/29_oct_2026/WS_and_Datacards/

echo
echo "  Checking the fit parameters..."
python3 check_fit_para.py

# run combine to perform the fit
echo
echo "  Running combine to perform the fit..."
combine -M MultiDimFit Datacard_tth_th_cp_Analysis_cpTopHiggs.root \
        --algo grid --points 50 \
        -m 125 \
        -t -1 \
        --setParameterRanges mu_ttH=0.00,4.0:fcp=0.0,1.0 \
        --setParameters mu_ttH=1,fcp=0,kappa_V=1 \
        --freezeParameters MH,kappa_V \
        --trackParameters mu_ttH \
        --alignEdges true \
        --saveNLL \
        --cminDefaultMinimizerStrategy 0 \
        --X-rtd MINIMIZER_analytic \
        --verbose 2 \

# Create one 1d scan
echo
echo "  Creating 1D scan of fcp..."
python3 Plot_LL_scan.py