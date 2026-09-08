#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024") # "2023preBPix" "2023postBPix" "2024")
cats=("tHq_had0_CP_even" "ttH_had0_CP_even" "ttH_had0_CP_odd" "tHq_had0_CP_mix")
# if you are adding new categories, make sure it is also addded to tools/replacementMap.py and the config file of every year
procs=("GG2H" "TTH" "tHqHadCPodd" "tHqHad" "tHqLepCPodd" "tHqLep",tHqHadKt0Ktt0,tHqHadKtm1Ktt0,tHqLepKt0Ktt0,tHqLepKtm1Ktt0)
# if you are adding new processes, make sure it is also addded to club_workspaces.sh and tool/XSBRMap.py is updated 

# for year in ${years[@]}; do
#     echo ${year}
#     F-test
#     python3 RunSignalScripts.py --inputConfig config_${year}.py --mode fTest --modeOpts "--doPlots"

#     Calculating the photon shape systematics
#     python3 RunSignalScripts.py --inputConfig config_${year}.py --mode calcPhotonSyst 

#     Signal fit
#     python3 RunSignalScripts.py \
#         --inputConfig config_${year}.py \
#         --mode signalFit \
#         --modeOpts "--useDCB --doPlots --skipSystematics --replacementThreshold 10 --skipVertexScenarioSplit --nBins 160 "  \
#         --groupSignalFitJobsByCat
# done

##  The packager merges each category's separate per-process, 
##  per-year signal-fit ROOT files into one combined workspace, 
##  so RunPlotter.py/the datacard have a single file per category 
##  to read from instead of dozens.

# # run the packager (merges across all years in one call, so runs once, outside the year loop)
# for cat in "${cats[@]}"; do
#     python3 RunPackager.py --cats "${cat}" --exts tth_th_cp_Analysis --mergeYears --batch local --massPoints 125
# done

# # Plotting the packaged signal model for each year and category
# # This way the script reweights each contributing process's fit 
# # (dropping any <0.1% of category yield) to its true xs×BR×eff×lumi normalization, 
# # then sums both the MC event points and fitted curves across all processes — 
# # so the plot shows the total expected signal shape for that category/year, not any single process.

# for year in ${years[@]}; do
#     echo ${year}
#     # Signal model plots
#     for cat in "${cats[@]}"; do
#         python3 RunPlotter.py --procs all --years "${year}" --cats "${cat}" --ext packaged
#     done
# done


# Plotting the packaged signal model for each year,category and process by process
for year in ${years[@]}; do 
    for proc in ${procs[@]}; do
        echo ${proc}
        for cat in "${cats[@]}"; do 
            echo ${cat}
            python3 RunPlotter.py \
            --procs ${proc} \
            --years ${year} \
            --cats $cat \
            --ext packaged  
        done
    done
done


# Running the packager for year if needed
# python3 RunPackager.py --cats ttH_had0_CP_even,ttH_had0_CP_mix,ttH_had0_CP_odd,ttH_had1_CP_even,ttH_had1_CP_mix,ttH_had1_CP_odd,ttH_lep0_CP_even,ttH_lep0_CP_mix,ttH_lep0_CP_odd,ttH_lep1_CP_even,ttH_lep1_CP_mix,ttH_lep1_CP_odd --exts tth_th_cp_Analysis_${year} --mergeYears --batch local --massPoints 125


