#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024") # "2023preBPix" "2023postBPix" "2024")
for year in ${years[@]}; do
    echo ${year}
    # F-test
    #python3 RunSignalScripts.py --inputConfig config_${year}.py --mode fTest --modeOpts "--doPlots"

    # Calculating the photon shape systematics
    # python3 RunSignalScripts.py --inputConfig config_${year}.py --mode calcPhotonSyst 

    # Signal fit
    # python3 RunSignalScripts.py --inputConfig config_${year}.py --mode signalFit --modeOpts "--useDCB --doPlots --skipSystematics --replacementThreshold 10 --skipVertexScenarioSplit --nBins 160 "  --groupSignalFitJobsByCat
    
    #Signal model plots
    # for cat in ttH_had0_CP_even ttH_had0_CP_odd ; do python3 RunPlotter.py --procs all --years 2022preEE --cats $cat --ext packaged ; done
done

# Running the packager#
# python3 RunPackager.py --cats ttH_had0_CP_even,ttH_had0_CP_mix,ttH_had0_CP_odd,ttH_had1_CP_even,ttH_had1_CP_mix,ttH_had1_CP_odd,ttH_lep0_CP_even,ttH_lep0_CP_mix,ttH_lep0_CP_odd,ttH_lep1_CP_even,ttH_lep1_CP_mix,ttH_lep1_CP_odd --exts tth_th_cp_Analysis_${year} --mergeYears --batch local --massPoints 125
# python3 RunPackager.py --cats ttH_had0_CP_even,ttH_had0_CP_odd --exts tth_th_cp_Analysis --batch local --massPoints 125 --mergeYears

#  Signal model plots
# for cat in ttH_had0_CP_even ttH_had0_CP_odd ; do 
#     python3 RunPlotter.py \
#      --procs GG2H,TTH,tHqHadCPodd,tHqHad,tHqLepCPodd,tHqLep \
#     --years 2022preEE \
#     --cats $cat \
#     --ext packaged  
# done