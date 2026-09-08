#!/bin/bash
# Shares the already-built datacard + signal/background workspaces by rsync'ing them
# to a public eos location, under a folder tagged with today's date.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MOVE_DIR="/eos/home-m/mikumar/php-plots/tth_analysis/Final_fits/"
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0 [--dir DEST_DIR]"
            echo
            echo "  Rsync the datacard and background + signal workspaces to"
            echo "  DEST_DIR/<day_mon_year>/WS_and_Datacards/{,Models/{background,signal}}/"
            echo "  (date tag is today's date)"
            echo "  --dir DEST_DIR   Destination base directory (default: ${MOVE_DIR})"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        --dir)
            MOVE_DIR="$2"
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
    shift
done

cd "${SCRIPT_DIR}"

DATE_TAG=$(/usr/bin/date "+%-d_%b_%Y" | tr 'A-Z' 'a-z')
WS_DIR="${MOVE_DIR%/}/${DATE_TAG}/WS_and_Datacards"
DEST_BASE="${WS_DIR}/Models"
mkdir -p "${DEST_BASE}/background/" "${DEST_BASE}/signal/"
rsync -av Datacard_tth_th_cp_Analysis.* "${WS_DIR}/"
rsync -av ../Background/outdir_tth_th_cp_Analysis/ "${DEST_BASE}/background/"
rsync -av ../Background/plots_tth_th_cp_Analysis "${DEST_BASE}/background/"
rsync -av ../Signal/outdir_packaged/ "${DEST_BASE}/signal/"
