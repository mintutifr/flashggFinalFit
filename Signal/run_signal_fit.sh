#!/bin/bash

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

# F-test
python3 RunSignalScripts.py --inputConfig config_2022preEE.py --mode fTest --modeOpts "--doPlots" 

# # Calculating the photon shape systematics
# python3 RunSignalScripts.py --inputConfig config_tutorial_2022preEE.py --mode calcPhotonSyst 

# # Signal fit
# python3 RunSignalScripts.py --inputConfig config_2022preEE.py --mode signalFit --modeOpts "--doPlots --skipSystematics --replacementThreshold 10 --skipVertexScenarioSplit"  --groupSignalFitJobsByCat

# # Running the packager#
# python3 RunPackager.py --cats ttH_had_CP_even,tH_had_CP_even --exts tth_th_cp_Analysis_2022preEE --mergeYears --batch local --massPoints 125

# #Signal model plots
# for cat in ttH_had_CP_even tH_had_CP_even; do python3 RunPlotter.py --procs all --years 2022preEE --cats $cat --ext packaged; done



