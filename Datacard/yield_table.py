#!/usr/bin/env python3
# Print nominal_yield and true_yield side by side, for any year and/or category.
#  * --cat omitted  -> every category found in --dir (all *.pkl files)
#  * --year omitted -> every year found in the selected category(ies)
#
# nominal_yield is read straight from the yields pkl (eff*acc only). true_yield
# reproduces Datacard/makeDatacard.py's --prune formula (true_yield = xsbr*ea*rate,
# Datacard/makeDatacard.py:102-117) using Datacard/tools/XSBR.py - the same code
# path as Plots/makeYieldsTables_tthth.py --trueYield.

import os
import glob
import pickle
import argparse

import pandas as pd

from tools.XSBR import extractXSBR

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def load_categories(yields_dir, cats):
    if cats is None:
        pkl_files = sorted(glob.glob(os.path.join(yields_dir, "*.pkl")))
        if not pkl_files:
            raise FileNotFoundError(f"No .pkl files found in {yields_dir}")
    else:
        pkl_files = []
        for cat in cats:
            pkl_file = os.path.join(yields_dir, f"{cat}.pkl")
            if not os.path.isfile(pkl_file):
                print(f"Warning: category '{cat}' not found ({pkl_file}). Skipping.")
                continue
            pkl_files.append(pkl_file)

    frames = []
    for f in pkl_files:
        with open(f, "rb") as fin:
            frames.append(pickle.load(fin))
    return pd.concat(frames, ignore_index=True)


def add_true_yield(df, mass, analysis):
    """Add xsbr/ea/true_yield columns, mirroring makeDatacard.py's --prune formula."""

    sigMask = df["type"] == "sig"
    XSBR = extractXSBR(df, mass=mass, analysis=analysis)

    df["xsbr"] = "-"
    df.loc[sigMask, "xsbr"] = df[sigMask].apply(lambda x: XSBR["XS_%s" % x["procOriginal"]] * XSBR["BR"], axis=1)

    df["ea"] = "-"
    df.loc[sigMask, "ea"] = df.loc[sigMask, "nominal_yield"]

    df["true_yield"] = "-"
    df.loc[sigMask, "true_yield"] = df[sigMask].apply(lambda x: x["xsbr"] * x["ea"] * x["rate"], axis=1)

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Print nominal_yield and true_yield (XS*BR*lumi-scaled) for any year/category."
    )
    parser.add_argument("-d", "--dir", default="yields_tth_th_cp_Analysis", help="Directory of per-category .pkl files")
    parser.add_argument("-c", "--cat", nargs="+", default=None, help="One or more category names (without .pkl). Default: every category in --dir")
    parser.add_argument("-y", "--year", nargs="+", default=None, help="One or more years, e.g. 2022preEE 2024. Default: every year present")
    parser.add_argument("--mass", default="125", help="MH mass, used to look up XS*BR")
    parser.add_argument("--analysis", default="tth_th_cp_Analysis", help="Analysis name in Datacard/tools/XSBR.py's XSBRMap")
    parser.add_argument("-o", "--out", default=None, help="Also write the table to this txt file")
    args = parser.parse_args()

    df = load_categories(args.dir, args.cat)
    df = add_true_yield(df, args.mass, args.analysis)

    sig = df[df["type"] == "sig"].copy()
    if args.year is not None:
        sig = sig[sig["year"].isin(args.year)]
        missingYears = set(args.year) - set(sig["year"].unique())
        if missingYears:
            print(f"Warning: no rows found for year(s): {', '.join(sorted(missingYears))}")

    if len(sig) == 0:
        print("No rows match the given --cat/--year selection.")
        return

    rows = sig[["cat", "year", "procOriginal", "nominal_yield", "true_yield"]].sort_values(["cat", "year", "procOriginal"])
    lines = [rows.to_string(index=False)]

    totals = sig.groupby("cat")[["nominal_yield", "true_yield"]].sum()
    totals.loc["Total (all selected categories)"] = totals.sum()
    lines.append("")
    lines.append(f"-- Totals (sum over {'all years' if args.year is None else ', '.join(args.year)}) --")
    lines.append(totals.to_string())

    out = "\n".join(lines)
    print(out)

    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
        print(f"\nCreated: {args.out}")


if __name__ == "__main__":
    main()
