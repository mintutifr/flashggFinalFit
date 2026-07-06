#!/usr/bin/env python3

import os
import glob
import pickle
import argparse
import pandas as pd

# Ensure all columns are written
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 1000)

COLUMNS_TO_SKIP = [
    "inputWSFile",
    "nominalDataName",
    "modelWSFile",
    "model",
    "proc"
]

import pandas as pd

def compute_yearly_sums_from_txt(txt_file, columns_to_sum=None):
    """
    Read txt file and compute per-year sums for a list of columns.
    
    Parameters
    ----------
    txt_file : str
        Input txt file
    columns_to_sum : list[str]
        Columns to compute sums for (easy to extend)
    """

    if columns_to_sum is None:
        columns_to_sum = ["nominal_yield", "sumw2"]

    # read table
    df = pd.read_csv(txt_file, sep=r"\s+", engine="python")

    # ensure year exists
    if "year" not in df.columns:
        raise ValueError("Column 'year' not found in file")

    # convert requested columns safely
    valid_cols = []
    for col in columns_to_sum:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            valid_cols.append(col)
        else:
            print(f"⚠️ Warning: column '{col}' not found, skipping")

    if not valid_cols:
        raise ValueError("No valid columns found to sum")

    # group by year and sum
    result = df.groupby("year")[valid_cols].sum()

    return result

def write_yearly_summary(txt_file, columns_to_sum=None):
    result = compute_yearly_sums_from_txt(txt_file, columns_to_sum)

    out_file = txt_file.replace(".txt", "_yearly_summary.txt")

    with open(out_file, "w") as f:
        f.write(result.to_string())

    print(f"Created: {out_file}")

def dump_pickle(pkl_file):
    """Load a pickle file and dump its contents to a text file."""

    with open(pkl_file, "rb") as f:
        data = pickle.load(f)

    txt_file = os.path.splitext(pkl_file)[0] + ".txt"

    with open(txt_file, "w") as out:

        if isinstance(data, pd.DataFrame):

            # drop only columns that exist
            cols_to_drop = [c for c in COLUMNS_TO_SKIP if c in data.columns]
            filtered = data.drop(columns=cols_to_drop)

            out.write(filtered.to_string(index=False))

        else:
            out.write(str(data))

    print(f"Created: {txt_file}")
    write_yearly_summary(
        txt_file,
        columns_to_sum=["nominal_yield", "sumw2"]
    )


def main():
    parser = argparse.ArgumentParser(
    description="Convert pickle DataFrames to text files."
    )

    parser.add_argument(
        "-d", "--dir",
        required=True,
        help="Directory containing .pkl files"
    )

    parser.add_argument(
        "-c", "--cat",
        nargs="+",
        default=None,
        help="One or more category names (without .pkl). If omitted, process all .pkl files."
    )

    args = parser.parse_args()

    directory = args.dir
    category = args.cat

    print(f"looking in dir {directory}")

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    if category is None:
        pkl_files = sorted(glob.glob(os.path.join(directory, "*.pkl")))

        if not pkl_files:
            print("No .pkl files found.")
            return
    else:
        pkl_files = []
        for cat in category:
            pkl_file = os.path.join(directory, f"{cat}.pkl")

            if not os.path.isfile(pkl_file):
                print(f"Warning: category '{cat}' not found ({pkl_file}). Skipping.")
                continue

            pkl_files.append(pkl_file)
    
    for pkl_file in pkl_files:
        print(f"\n dumping yields from {category}")
        dump_pickle(pkl_file)


if __name__ == "__main__":
    main()