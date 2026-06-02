#!/bin/bash

# Optional: stop on error
set -e

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

# Run your command
python3 trees2ws.py \
  --inputConfig config_tutorial.py \
  --inputTreeFile outputForFinalFits_Test/root/ttH_2022preEE/output_TTHToGG_M125_13TeV_amcatnlo_pythia8.root \
  --inputMass 125 \
  --productionMode tth \
  --year 2022preEE \
  #--doSystematics
