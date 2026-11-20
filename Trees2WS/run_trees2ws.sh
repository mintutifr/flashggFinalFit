#!/bin/bash

# Optional: stop on error
set -e

# load setup environment if needed
export PYTHONNOUSERSITE=1
source ../setup.sh

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 [--data]"
    echo
    echo "  (no args)   Run trees2ws.py over the MC samples (default)"
    echo "  --data      Run trees2ws_data.py over Data/allData.root"
    echo "  -h, --help  Show this help message"
    exit 0
elif [[ "$1" == "--data" ]]; then
    # Run Data command
    python3 trees2ws_data.py \
      --inputConfig config_tutorial.py \
      --inputTreeFile /eos/user/m/mikumar/Final_fits/outputForFinalFits_18Nov2026/root/Data/allData.root \
      --applyMassCut --massCutRange 100,180
else
    years=("2022preEE" "2022postEE" "2023preBPix" "2023postBPix" "2024")
    samples=("ttH" "ttH_CPodd" "tHqHad" "tHqHad_CPodd" "tHqLep" "tHqLep_CPodd" "GluGluH" "tHqHad_Kt0Ktt0" "tHqHad_Ktm1Ktt0" "tHqLep_Kt0Ktt0" "tHqLep_Ktm1Ktt0" "bbH" "VBFH" "VH" "tHW")
    production_mode=("tth" "tthCPodd" "tHqHad" "tHqHadCPodd" "tHqLep" "tHqLepCPodd" "ggh" "tHqHadKt0Ktt0" "tHqHadKtm1Ktt0" "tHqLepKt0Ktt0" "tHqLepKtm1Ktt0" "bbh" "vbf" "vh" "tHW")
    yaml_file="outputfiles.yaml"

    # Build the list of trees2ws.py calls first (the skip-check and YAML
    # lookup are cheap, so keep those sequential), then run them in
    # parallel sample-year, fully independent.
    CMDS_FILE=$(mktemp)
    trap 'rm -f "${CMDS_FILE}"' EXIT

    for i in "${!samples[@]}"; do
        sample="${samples[$i]}"
        prod_mode="${production_mode[$i]}"
        sample_key="${sample//_/}"
        outputfile=$(python3 -c "import yaml; print(yaml.safe_load(open('$yaml_file'))['$sample_key'])")
        echo ${outputfile}
        for year in "${years[@]}"; do
            inputTreeFile="/eos/user/m/mikumar/Final_fits/outputForFinalFits_18Nov2026/root/${sample}_${year}/${outputfile}"
            if [[ ! -f "${inputTreeFile}" ]]; then
                echo "  [SKIP] Missing: ${inputTreeFile}"
                continue
            fi
            echo "python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile '${inputTreeFile}' --inputMass 125 --productionMode ${prod_mode} --year ${year}" >> "${CMDS_FILE}"
        done
    done

    echo
    echo "Running $(wc -l < "${CMDS_FILE}") trees2ws.py conversions (up to 8 in parallel)..."
    xargs -P 8 -I{} bash -c '{}' < "${CMDS_FILE}"
fi
