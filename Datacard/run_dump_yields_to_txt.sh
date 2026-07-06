#!/bin/bash

export PYTHONNOUSERSITE=1
source ../setup.sh

python3 dump_yields_to_txt.py \
    --dir yields_tth_th_cp_Analysis/ \
    --cat ttH_had0_CP_even ttH_had0_CP_odd
