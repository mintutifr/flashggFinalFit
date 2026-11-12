#!/bin/bash
# Runs count_mc_events.py once per category (each its own python3 process, to
# avoid a PyROOT memory leak from repeatedly opening RooWorkspace files in one
# long-lived process - see the note at the top of count_mc_events.py).
# Output per category: yields_tth_th_cp_Analysis/<cat>_numEvents.txt and
# <cat>_numEvents_yearly_summary.txt.

export PYTHONNOUSERSITE=1
source ../setup.sh

cats=("ttH_had0_CP_even" "ttH_had0_CP_odd" "ttH_had0_CP_mix" \
      "ttH_had1_CP_even" "ttH_had1_CP_odd" "ttH_had1_CP_mix" \
      "ttH_lep0_CP_even" "ttH_lep0_CP_odd" "ttH_lep0_CP_mix" \
      "ttH_lep1_CP_even" "ttH_lep1_CP_odd" "ttH_lep1_CP_mix" \
      "tHq_had0_CP_even" "tHq_had0_CP_odd" "tHq_had0_CP_mix" \
      "tHq_had1_CP_even" "tHq_had1_CP_odd" "tHq_had1_CP_mix" \
      "tHq_lep0_CP_even" "tHq_lep0_CP_odd" "tHq_lep0_CP_mix" \
      "tHq_lep1_CP_even" "tHq_lep1_CP_odd" "tHq_lep1_CP_mix")

for cat in "${cats[@]}"; do
    echo "===== ${cat} ====="
    python3 count_mc_events.py --dir yields_tth_th_cp_Analysis/ --cat "${cat}"
done
