#!/bin/bash
# Master pipeline for the ttH/tH CP analysis final fits.
# Chains together the individual step scripts (Trees2WS -> Signal -> Background -> Datacard).
# Run with cmsenv available (sources setup.sh below).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Step registry: each step is a unique KEY (not a number), with a description
# and a step_<KEY>() function. Run order is set once, below, in STEP_ORDER.
#
# To add a step, anywhere in the pipeline:
#   1. Pick a new unique key and add STEP_DESC[key]=... + step_key() { ... }.
#   2. Insert that key into STEP_ORDER at the position you want it to run.
# No existing key, description, function, or STEP_ORDER entry needs to change
# -- display numbers are derived automatically from position in STEP_ORDER.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
declare -A STEP_DESC

STEP_DESC[trees2ws_mc]="Trees2WS MC - ./Trees2WS/run_trees2ws.sh (convert HiggsDNA  MC trees to RooWorkspaces)"
step_trees2ws_mc() {
    pushd "${SCRIPT_DIR}/Trees2WS" > /dev/null
    ./run_trees2ws.sh
    popd > /dev/null
}

STEP_DESC[trees2ws_data]="Trees2WS data - ./Trees2WS/run_trees2ws.sh --data (convert HiggsDNA Data trees to RooWorkspaces)"
step_trees2ws_data() {
    pushd "${SCRIPT_DIR}/Trees2WS" > /dev/null
    ./run_trees2ws.sh --data
    popd > /dev/null
}

STEP_DESC[club_workspaces]="Club workspaces - ./Signal/club_workspaces.sh (collect per-sample ws_* root files into workspaces/<year>/)"
step_club_workspaces() {
    pushd "${SCRIPT_DIR}/Signal" > /dev/null
    ./club_workspaces.sh
    popd > /dev/null
}

STEP_DESC[signal]="Signal - ./Signal/run_signal_fit.sh (signal fits, packaging, plots)"
step_signal() {
    pushd "${SCRIPT_DIR}/Signal" > /dev/null
    ./run_signal_fit.sh
    popd > /dev/null
}

STEP_DESC[plot_background]="Plot background - python3 Background/Plot_background.py --cat all (pre-fit background shape, all categories)"
step_plot_background() {
    pushd "${SCRIPT_DIR}/Background" > /dev/null
    python3 Plot_background.py --cat all
    popd > /dev/null
}

STEP_DESC[background]="Background - ./Background/run_Background_fit.sh (background F-test)"
step_background() {
    pushd "${SCRIPT_DIR}/Background" > /dev/null
    ./run_Background_fit.sh
    popd > /dev/null
}

STEP_DESC[create_yields]="Create yields - ./Datacard/run_create_yields.sh (RunYields.py per category, no pruning/datacard yet)"
step_create_yields() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_create_yields.sh
    popd > /dev/null
}

STEP_DESC[yields_table]="Yields table - ./Datacard/run_makeYieldsTables_tthth.sh (build the CP analysis yields/purity table, nominal_yield and true_yield)"
step_yields_table() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_makeYieldsTables_tthth.sh
    ./run_makeYieldsTables_tthth.sh --trueYield
    popd > /dev/null
}

STEP_DESC[event_counts]="Event counts - ./Datacard/run_count_mc_events.sh (raw MC event counts per category, one process per category)"
step_event_counts() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_count_mc_events.sh
    popd > /dev/null
}

STEP_DESC[event_counts_table]="Event counts table - ./Datacard/run_makeEventTables_tthth.sh (build the CP analysis MC event-count table)"
step_event_counts_table() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_makeEventTables_tthth.sh
    popd > /dev/null
}

STEP_DESC[build_datacard]="Build datacard - ./Datacard/run_build_datacard.sh (makeDatacard.py: pruning, systematics, write the datacard)"
step_build_datacard() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_build_datacard.sh
    popd > /dev/null
}

STEP_DESC[move]="Move - ./Datacard/run_move_file_to_eos.sh (share the datacard + workspaces on eos)"
step_move() {
    pushd "${SCRIPT_DIR}/Datacard" > /dev/null
    ./run_move_file_to_eos.sh
    popd > /dev/null
}

STEP_DESC[plot_shape]="Plot - python3 Datacard/plot_shape.py (plot the signal PDF shape)"
step_plot_shape() {
    pushd "${SCRIPT_DIR}" > /dev/null
    python3 Datacard/plot_shape.py
    popd > /dev/null
}

STEP_DESC[combine]="Combine - /run_combine.sh (build the combine workspace and run the fit)"
step_combine() {
    pushd "${SCRIPT_DIR}/Combine" > /dev/null
    ./run_combine.sh
    popd > /dev/null
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run order. This is the ONLY place that encodes step ordering/numbering.
# Insert a key anywhere in this list to slot a new step into the sequence.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STEP_ORDER=(
    trees2ws_mc
    trees2ws_data
    club_workspaces
    signal
    plot_background
    background
    create_yields
    yields_table
    event_counts
    event_counts_table
    build_datacard
    move
    plot_shape
    combine
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Expand a --steps spec (e.g. "1", "1-3", "1,3", "1,3-5") into a sorted,
# deduplicated list of 1-based positions into STEP_ORDER.
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
            for i in "${!STEP_ORDER[@]}"; do
                n=$((i + 1))
                key="${STEP_ORDER[$i]}"
                echo "  Step ${n}: ${STEP_DESC[$key]}"
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
    STEPS_TO_RUN=()
    for i in "${!STEP_ORDER[@]}"; do STEPS_TO_RUN+=("$((i + 1))"); done
fi

for n in "${STEPS_TO_RUN[@]}"; do
    if [[ -z "${STEP_ORDER[$((n - 1))]:-}" ]]; then
        echo "[ERROR] No such step: ${n}" >&2
        exit 1
    fi
done

set -e

export PYTHONNOUSERSITE=1
source "${SCRIPT_DIR}/setup.sh"

for n in "${STEPS_TO_RUN[@]}"; do
    key="${STEP_ORDER[$((n - 1))]}"
    echo "===== STEP ${n}: ${STEP_DESC[$key]} ====="
    "step_${key}"
done

echo "===== PIPELINE COMPLETE ====="
