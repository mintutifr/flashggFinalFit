#!/bin/bash
# Updates every hardcoded reference to the date-stamped input/output
# directory name across the pipeline files that use it.
#
# Usage: ./update_input_dir.sh <old_name> <new_name>
# Example:
#   ./update_input_dir.sh outputForFinalFits_29Oct2026 outputForFinalFits_18Nov2026
#
# The file list below was checked against a repo-wide grep for both the full
# name and the bare date string - if you add a new script that hardcodes this
# path, add it here too.

if [[ "$#" -ne 2 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    echo "Usage: $0 <old_name> <new_name>"
    echo
    echo "  Replaces every occurrence of <old_name> with <new_name> in the"
    echo "  files below (the ones that hardcode the date-stamped input/output"
    echo "  directory name)."
    echo
    echo "  Example: $0 outputForFinalFits_29Oct2026 outputForFinalFits_18Nov2026"
    echo "  -h, --help   Show this help message"
    exit 0
fi

OLD_NAME="$1"
NEW_NAME="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FILES=(
    "Background/Plot_background.py"
    "Background/config_DataCombine.py"
    "Datacard/run_create_yields.sh"
    "Signal/club_workspaces.sh"
    "Signal/config_2022postEE.py"
    "Signal/config_2022preEE.py"
    "Signal/config_2023postBPix.py"
    "Signal/config_2023preBPix.py"
    "Signal/config_2024.py"
    "Trees2WS/run_trees2ws.sh"
)

echo "===== Replacing '${OLD_NAME}' with '${NEW_NAME}' ====="

for f in "${FILES[@]}"; do
    full="${SCRIPT_DIR}/${f}"
    if [[ ! -f "${full}" ]]; then
        echo " --> [WARNING] ${f}: file not found, skipping" >&2
        continue
    fi
    n=$(grep -c "${OLD_NAME}" "${full}")
    if [[ "${n}" -eq 0 ]]; then
        echo " --> [WARNING] ${f}: no occurrences of '${OLD_NAME}' found, skipping" >&2
        continue
    fi
    sed -i "s|${OLD_NAME}|${NEW_NAME}|g" "${full}"
    echo " --> ${f}: replaced ${n} occurrence(s)"
done

echo
echo "===== DONE ====="
echo "Verify with: grep -rn \"${OLD_NAME}\" \"${SCRIPT_DIR}\""
