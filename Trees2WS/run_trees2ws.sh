#!/bin/bash

# Optional: stop on error
set -e

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024")
samples=("ttH" "tHqHad" "tHqLep" "GluGluH")
production_mode=("tth" "tHqHad" "tHqLep" "ggh")
yaml_file="outputfiles.yaml"

# Run MC command
# for i in "${!samples[@]}"; do
#     sample="${samples[$i]}"
#     prod_mode="${production_mode[$i]}"
#     outputfile=$(python3 -c "import yaml; print(yaml.safe_load(open('$yaml_file'))['$sample'])")
#     echo ${outputfile}
#     for year in "${years[@]}"; do
#         python3 trees2ws.py \
#           --inputConfig config_tutorial.py \
#           --inputTreeFile /eos/user/m/mikumar/Final_fits/outputForFinalFits_25June2026/root/${sample}_${year}/${outputfile} \
#           --inputMass 125 \
#           --productionMode ${prod_mode} \
#           --year ${year} \
#           #--doSystematics
#     done
# done

# Run Data command
python3 trees2ws_data.py \
  --inputConfig config_tutorial.py \
  --inputTreeFile /eos/user/m/mikumar/Final_fits/outputForFinalFits_25June2026/root//Data/allData.root \
  --applyMassCut --massCutRange 100,180
