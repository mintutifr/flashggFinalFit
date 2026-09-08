#!/bin/bash

# Base input directory
INPUT_BASE="/eos/user/m/mikumar/Final_fits/outputForFinalFits_7Sep2026/root"

# Base output directory
OUTPUT_BASE="/eos/user/m/mikumar/Final_fits/outputForFinalFits_7Sep2026/workspaces"

# Sample list
samples=(
    "GluGluH"
    "ttH"
    "ttH_CPodd"
    "tHqHad"
    "tHqHad_CPodd"
    "tHqLep"
    "tHqLep_CPodd"
    "tHqHad_Kt0Ktt0"
    "tHqHad_Ktm1Ktt0"
    "tHqLep_Kt0Ktt0"
    "tHqLep_Ktm1Ktt0"
    # "tHW"
    # "tHW_CPodd"
)

# Era list
eras=(
    "2022preEE"
    "2022postEE"
    "2023preBPix"
    "2023postBPix"
    "2024"
)

# Create output base directory if it doesn't exist
mkdir -p "${OUTPUT_BASE}"

for era in "${eras[@]}"; do
    echo "Processing era: ${era}"

    # Create era-specific output directory
    ERA_OUT="${OUTPUT_BASE}/${era}"
    mkdir -p "${ERA_OUT}"

    for sample in "${samples[@]}"; do
        SRC_DIR="${INPUT_BASE}/${sample}_${era}"

        # Check if source directory exists
        if [[ ! -d "${SRC_DIR}" ]]; then
            echo "  Missing: ${SRC_DIR}"
            continue
        fi

        # Find ws_* directories and copy root files
        for wsdir in "${SRC_DIR}"/ws_*; do
            if [[ -d "${wsdir}" ]]; then
                echo "  Copying from ${wsdir}"

                find "${wsdir}" -maxdepth 1 -name "*.root" -exec cp {} "${ERA_OUT}/" \;
            fi
        done
    done
done
echo
echo "Done collecting all workspace ROOT files to ${OUTPUT_BASE}."