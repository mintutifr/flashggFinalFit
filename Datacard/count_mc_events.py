#!/usr/bin/env python3
# Report raw (unweighted) MC event counts alongside nominal_yield for the signal
# processes in a category's yields pkl (same pkl files read by
# Plots/makeYieldsTables_tthth.py in pipeline Step 7 / Datacard/run_dump_yields_to_txt.sh).
#
# The pkl only stores nominal_yield (sum of per-event weights) - it never stores
# the raw event count, so this reopens each row's input ROOT workspace
# (inputWSFile/nominalDataName columns, already in the pkl) and calls
# RooDataSet.numEntries() to get it.
#
# NOTE: repeatedly opening many RooWorkspace-containing ROOT files in one long-lived
# process leaks memory in PyROOT. Run this once per category (see
# run_count_mc_events.sh, which invokes a fresh python3 process per category, same
# as Datacard/run_create_yields.sh does for RunYields.py) rather than passing a
# long --cat list / omitting --cat to process every category in a single call.

import os
import glob
import pickle
import argparse

import ROOT
import pandas as pd

from commonObjects import inputWSName__

ROOT.gROOT.SetBatch(True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def count_events(pkl_file):
    """Load a pickle file and return a DataFrame of numEntries/nominal_yield per signal row."""

    with open(pkl_file, "rb") as f:
        data = pickle.load(f)

    sig = data[data["type"] == "sig"].copy()

    numEntries = []
    for _, r in sig.iterrows():
        f_in = ROOT.TFile.Open(r["inputWSFile"])
        ws = f_in.Get(inputWSName__)
        d = ws.data(r["nominalDataName"])
        numEntries.append(d.numEntries())
        f_in.Close()

    sig["numEntries"] = numEntries

    return sig[["year", "type", "procOriginal", "cat", "numEntries", "nominal_yield"]]


def write_report(pkl_file):
    result = count_events(pkl_file)

    txt_file = os.path.splitext(pkl_file)[0] + "_numEvents.txt"
    with open(txt_file, "w") as f:
        f.write(result.to_string(index=False))
    print(f"Created: {txt_file}")

    summary = result.groupby("year")[["numEntries", "nominal_yield"]].sum()
    summary.loc["Total"] = summary.sum()

    summary_file = os.path.splitext(pkl_file)[0] + "_numEvents_yearly_summary.txt"
    with open(summary_file, "w") as f:
        f.write(summary.to_string())
    print(f"Created: {summary_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Report raw MC event counts (numEntries) alongside nominal_yield for signal pkl files."
    )
    parser.add_argument("-d", "--dir", required=True, help="Directory containing .pkl files")
    parser.add_argument(
        "-c", "--cat",
        nargs="+",
        default=None,
        help="One or more category names (without .pkl). If omitted, process all .pkl files "
             "(NOT recommended in one call for more than ~1 category - see memory-leak note above)."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        raise FileNotFoundError(f"Directory not found: {args.dir}")

    if args.cat is None:
        pkl_files = sorted(glob.glob(os.path.join(args.dir, "*.pkl")))
        if not pkl_files:
            print("No .pkl files found.")
            return
    else:
        pkl_files = []
        for cat in args.cat:
            pkl_file = os.path.join(args.dir, f"{cat}.pkl")
            if not os.path.isfile(pkl_file):
                print(f"Warning: category '{cat}' not found ({pkl_file}). Skipping.")
                continue
            pkl_files.append(pkl_file)

    for pkl_file in pkl_files:
        print(f"\n counting events from {pkl_file}")
        write_report(pkl_file)


if __name__ == "__main__":
    main()
