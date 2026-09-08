#!/bin/bash
# Master pipeline for the ttH/tH CP analysis final fits.
# Chains together the individual step scripts (Trees2WS -> Signal -> Background -> Datacard).
# Run with cmsenv available (sources setup.sh below).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Step definitions: to add a new step, add its description below and a
# matching step_N() function that performs it.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STEP_DESC[1]="Trees2WS - ./Trees2WS/run_trees2ws.sh (convert HiggsDNA trees to RooWorkspaces)"

step_1() {
    pushd "${SCRIPT_DIR}/Trees2WS" > /dev/null
    ./run_trees2ws.sh
    popd > /dev/null
}

STEP_DESC[2]="Signal - ./Signal/run_signal_fit.sh (signal fits, packaging, plots)"

step_2() {
    pushd "${SCRIPT_DIR}/Signal" > /dev/null
    ./run_signal_fit.sh
    popd > /dev/null
}

STEP_DESC[3]="Background - ./Background/run_Background_fit.sh (background F-test)"

step_3() {
    pushd "${SCRIPT_DIR}/Background" > /dev/null
    ./run_Background_fit.sh
    popd > /dev/null
}

STEP_DESC[4]="Datacard - ./Datacard/run_create_datacard.sh (build the datacard)"

step_4() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_create_datacard.sh
    popd > /dev/null
}

STEP_DESC[5]="Move - ./Datacard/run_move_file_to_eos.sh (share the datacard + workspaces on eos)"

step_5() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_move_file_to_eos.sh
    popd > /dev/null
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Expand a --steps spec (e.g. "1", "1-3", "1,3", "1,3-5") into a sorted,
# deduplicated list of step numbers.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
expand_steps() {
    local spec="$1"
    local part start end n
    IFS=',' read -ra parts <<< "${spec}"
    for part in "${parts[@]}"; do
        if [[ "${part}" == *-* ]]; then
            start="${part%-*}"
            end="${part#*-}"
            for ((n=start; n<=end; n++)); do echo "${n}"; done
        else
            echo "${part}"
        fi
    done | sort -n -u
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Argument parsing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STEPS_ARG=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0 [--steps LIST] [-h|--help]"
            echo
            echo "Runs the ttH/tH CP analysis final-fits pipeline, step by step:"
            for n in "${!STEP_DESC[@]}"; do
                echo "  Step ${n}: ${STEP_DESC[$n]}"
            done
            echo
            echo "  --steps LIST   Only run the given steps, e.g. '1', '1-3', '1,3', '1,3-5' (default: all)"
            echo "  -h, --help     Print the pipeline steps above and exit without running anything"
            exit 0
            ;;
        --steps)
            STEPS_ARG="$2"
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
    shift
done

if [[ -n "${STEPS_ARG}" ]]; then
    mapfile -t STEPS_TO_RUN < <(expand_steps "${STEPS_ARG}")
else
    STEPS_TO_RUN=("${!STEP_DESC[@]}")
fi

for n in "${STEPS_TO_RUN[@]}"; do
    if [[ -z "${STEP_DESC[$n]:-}" ]]; then
        echo "[ERROR] No such step: ${n}" >&2
        exit 1
    fi
done

set -e

export PYTHONNOUSERSITE=1
source "${SCRIPT_DIR}/setup.sh"

for n in "${STEPS_TO_RUN[@]}"; do
    echo "===== STEP ${n}: ${STEP_DESC[$n]} ====="
    "step_${n}"
done

echo "===== PIPELINE COMPLETE ====="
