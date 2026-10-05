#!/usr/bin/env python3
"""
Make the standard likelihood-scan plots from outputs/.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

try:
    import uproot
except ImportError:
    sys.exit("ERROR: uproot not found. Load/install uproot before running this plotting script.")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_DIR, "outputs")

CL68_1D = 1.00
CL95_1D = 3.84
CL68_2D = 2.30
CL95_2D = 5.99

# PLOTS = [
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_massfit_fixedKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_massfit_fixed.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ fixed)",
#     },
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_massfit_profiledKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_massfit_profiled.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled)",
#     },
#     {
#         "kind": "2d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_massfit.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan2d_massfit.pdf"),
#         "title": r"$t\bar{t}H$ CP coupling scan",
#     },
# ]

# PLOTS = [
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_fixedKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_fixed.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ fixed)",
#     },
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_profiledKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_profiled.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled)",
#     },
#     {
#         "kind": "2d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_tth_th_cp_Analysis_cat2.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan2d_tth_th_cp_Analysis_cat2.pdf"),
#         "title": r"$t\bar{t}H$ CP coupling scan",
#     },
# ]

# PLOTS = [
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_fixedKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_fixed.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ fixed)",
#         "x_branch": "kappa_tilde",
#         "x_label": r"$\tilde{\kappa}_t$",
#     },
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_profiledKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_profiled.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled)",
#         "x_branch": "kappa_tilde",
#         "x_label": r"$\tilde{\kappa}_t$",
#     },
#     {
#         "kind": "2d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_tth_th_cp_Analysis_cat2_allyear.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan2d_tth_th_cp_Analysis_cat2_allyear.pdf"),
#         "title": r"$t\bar{t}H$ CP coupling scan",
#         "x_branch": "kappa_t",
#         "y_branch": "kappa_tilde",
#         "x_label": r"$\kappa_t$",
#         "y_label": r"$\tilde{\kappa}_t$",
#         "rerun": "bash scripts/run_scan_2d.sh massfit",
#     },
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_cpgg_fixedKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_cpgg_fixed.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ fixed)",
#         "x_branch": "kappa_tilde",
#         "x_label": r"$\tilde{\kappa}_t$",
#     },
#     {
#         "kind": "1d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_cpgg_profiledKt.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan1d_cpgg_profiled.pdf"),
#         "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled)",
#         "x_branch": "kappa_tilde",
#         "x_label": r"$\tilde{\kappa}_t$",
#     },
#     {
#         "kind": "2d",
#         "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_cpgg.MultiDimFit.mH125.root"),
#         "output": os.path.join(OUT_DIR, "scan2d_cpgg.pdf"),
#         "title": r"legacy $t\bar{t}H$ gg CP coupling scan",
#         "x_branch": "kappa_t",
#         "y_branch": "kappa_tilde",
#         "x_label": r"$\kappa_t$",
#         "y_label": r"$\tilde{\kappa}_t$",
#         "rerun": "bash scripts/run_scan_2d.sh cpgg",
#     },
# ]

PLOTS = [
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_fixedKt.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_fixed.pdf"),
    #     "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ fixed)",
    #     "x_branch": "kappa_tilde",
    #     "x_label": r"$\tilde{\kappa}_t$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_profiledKt.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_profiled.pdf"),
    #     "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled)",
    #     "x_branch": "kappa_tilde",
    #     "x_label": r"$\tilde{\kappa}_t$",
    # },
    # {
    #     "kind": "2d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_tth_th_cp_Analysis_cat2_allyear_01_test.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan2d_tth_th_cp_Analysis_cat2_allyear_01_test.pdf"),
    #     "title": r"$t\bar{t}H$ CP coupling scan",
    #     "x_branch": "kappa_t",
    #     "y_branch": "kappa_tilde",
    #     "x_label": r"$\kappa_t$",
    #     "y_label": r"$\tilde{\kappa}_t$",
    #     "rerun": "bash scripts/run_scan_2d.sh TEST",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_freezeMass.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_freezeMass.pdf"),
    #     "title": r"1D scan of $\tilde{\kappa}_t$ ($\kappa_t$ profiled, mass frozen)",
    #     "x_branch": "kappa_tilde",
    #     "x_label": r"$\tilde{\kappa}_t$",
    # },
    # {
    #     "kind": "2d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_tth_th_cp_Analysis_cat4_kt_ktt.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan2d_tth_th_cp_Analysis_cat4_kt_ktt.pdf"),
    #     "title": r"$t\bar{t}H$ CP coupling scan (mass frozen)",
    #     "x_branch": "kappa_t",
    #     "y_branch": "kappa_tilde",
    #     "x_label": r"$\kappa_t$",
    #     "y_label": r"$\tilde{\kappa}_t$",
    #     "rerun": "bash scripts/run_scan_2d.sh cat4",
    # },

    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_ALT_fcp.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_ALT_fcp.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "x",
    #     "x_label": r"$f_{CP}$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_ALT_fcp_mu_2p44_frozen.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_ALT_fcp_mu_2p44_frozen.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu 2.44 frozen)",
    #     "x_branch": "x",
    #     "x_label": r"$f_{CP}$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_fcp_new_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    #     {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat2_allyear_01_test_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat2_allyear_01_test_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat4_fcp_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat4_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    #     {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_cat4_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "scan1d_tth_th_cp_Analysis_cat4_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },

    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_back_to_2_ttH_cats_fcp_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_back_to_2_ttH_cats", "scan1d_tth_th_cp_Analysis_back_to_2_ttH_cats_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    #     {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_back_to_2_ttH_cats_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_back_to_2_ttH_cats", "scan1d_tth_th_cp_Analysis_back_to_2_ttH_cats_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },
    # { 
    #     "kind": "2d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan2D_tth_th_cp_Analysis_back_to_2_ttH_cats.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_back_to_2_ttH_cats", "scan2d_tth_th_cp_Analysis_back_to_2_ttH_cats.pdf"),
    #     "title": r"$t\bar{t}H$ CP coupling scan (mass frozen)",
    #     "x_branch": "kappa_t",
    #     "y_branch": "kappa_tilde",
    #     "x_label": r"$\kappa_t$",
    #     "y_label": r"$\tilde{\kappa}_t$",
    #     "rerun": "bash scripts/run_scan_2d.sh back_to_2_ttH_cats",
    # },

    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_back_to_2_ttH_cats_NO_THQ_fcp_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_back_to_2_ttH_cats_NO_THQ", "scan1d_tth_th_cp_Analysis_back_to_2_ttH_cats_NO_THQ_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_back_to_2_ttH_cats_NO_THQ_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_back_to_2_ttH_cats_NO_THQ", "scan1d_tth_th_cp_Analysis_back_to_2_ttH_cats_NO_THQ_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_OLD_2_ttH_cats_NO_THQ_fcp_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_OLD_2_ttH_cats_NO_THQ", "scan1d_tth_th_cp_Analysis_OLD_2_ttH_cats_NO_THQ_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_OLD_2_ttH_cats_NO_THQ_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_OLD_2_ttH_cats_NO_THQ", "scan1d_tth_th_cp_Analysis_OLD_2_ttH_cats_NO_THQ_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_OLD_2_ttH_cats_WITH_THQ_fcp_fcp_new.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_OLD_2_ttH_cats_WITH_THQ", "scan1d_tth_th_cp_Analysis_OLD_2_ttH_cats_WITH_THQ_fcp_new.pdf"),
    #     "title": r"1D scan of $f_{CP}$ (mu free)",
    #     "x_branch": "fcp",
    #     "x_label": r"$f_{CP}$",
    # },
    # {
    #     "kind": "1d",
    #     "input": os.path.join(OUT_DIR, "higgsCombine.Scan1D_tth_th_cp_Analysis_OLD_2_ttH_cats_WITH_THQ_angle_angle.MultiDimFit.mH125.root"),
    #     "output": os.path.join(OUT_DIR, "2026_09_23_OLD_2_ttH_cats_WITH_THQ", "scan1d_tth_th_cp_Analysis_OLD_2_ttH_cats_WITH_THQ_angle.pdf"),
    #     "title": r"1D scan of $\alpha$ (q free)",
    #     "x_branch": "alpha",
    #     "x_label": r"$\alpha$",
    # },
    {
        "kind": "1d",
        "input": os.path.join(SCRIPT_DIR, "higgsCombineTest.MultiDimFit.mH125.root"),
        "output": os.path.join(SCRIPT_DIR, "scan1d_fcp.pdf"),
        "title": r"1D scan of $f_{CP}$ ($\mu_{ttH}$ profiled)",
        "x_branch": "fcp",
        "x_label": r"$f_{CP}$",
    },
]    


def apply_cms_matplotlib_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 13,
        "axes.labelsize": 15,
        "axes.titlesize": 13,
        "axes.linewidth": 1.1,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.minor.size": 3,
        "ytick.minor.size": 3,
        "legend.fontsize": 11,
        "savefig.bbox": "tight",
    })


def add_cms_label(ax):
    ax.text(0.02, 1.01, "CMS", transform=ax.transAxes, fontsize=16, fontweight="bold", va="bottom")
    ax.text(0.14, 1.01, "Private", transform=ax.transAxes, fontsize=14, fontstyle="italic", va="bottom")
    ax.text(0.98, 1.01, "13.6 TeV", transform=ax.transAxes, fontsize=13, ha="right", va="bottom")


def read_tree(path):
    if not os.path.isfile(path):
        print(f"SKIP: missing {path}")
        return None
    with uproot.open(path) as root_file:
        if "limit" not in root_file:
            raise RuntimeError(f"TTree 'limit' not found in {path}")
        return root_file["limit"].arrays(library="np")


def as_float_array(values):
    return np.asarray(values, dtype=float)


def scan_start_index(branches):
    if "quantileExpected" in branches and len(branches["quantileExpected"]) > 1:
        if float(branches["quantileExpected"][0]) < 0.0:
            return 1
    return 0


def add_crossings(ax, x_values, y_values, threshold, color):
    diff = y_values - threshold
    sign_changes = np.where(np.diff(np.sign(diff)) != 0)[0]
    for idx in sign_changes:
        x0, x1 = x_values[idx], x_values[idx + 1]
        y0, y1 = diff[idx], diff[idx + 1]
        if y1 == y0:
            continue
        x_cross = x0 - y0 * (x1 - x0) / (y1 - y0)
        ax.axvline(x_cross, color=color, ls="--", lw=0.8, alpha=0.6)


def plot_1d(config, branches):
    x_branch = config["x_branch"]
    if x_branch not in branches or "deltaNLL" not in branches:
        raise RuntimeError(f"Required branches missing in {config['input']}")

    start = scan_start_index(branches)
    x = as_float_array(branches[x_branch][start:])
    q = 2.0 * as_float_array(branches["deltaNLL"][start:])

    mask = np.isfinite(x) & np.isfinite(q)
    x = x[mask]
    q = q[mask]
    if x.size == 0:
        raise RuntimeError(f"No finite 1D scan points in {config['input']}")

    order = np.argsort(x)
    x = x[order]
    q = q[order]
    q = q - np.nanmin(q)

    best_idx = int(np.nanargmin(q))
    best_x = float(x[best_idx])

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.plot(x, q, marker="o", ms=3, lw=1.6, color="black", label=r"Scan")
    ax.axhline(CL68_1D, color="#1f77b4", ls="--", lw=1.4, label=r"68% CL")
    ax.axhline(CL95_1D, color="#d62728", ls="--", lw=1.4, label=r"95% CL")
    ax.axvline(best_x, color="black", lw=1.0, ls=":", label="Best fit")
    ax.axvline(0.0, color="#DAA520", lw=1.5, ls="-", label="SM")
    add_crossings(ax, x, q, CL68_1D, "#1f77b4")
    add_crossings(ax, x, q, CL95_1D, "#d62728")
    ax.set_xlabel(config["x_label"])
    ax.set_ylabel(r"$-2\Delta\ln\mathcal{L}$")
    ax.set_title(config["title"])
    ax.set_ylim(0.0, max(10.0, float(np.nanmax(q)) * 1.1))
    ax.grid(True, which="major", alpha=0.25)
    ax.legend(loc="upper center", frameon=False, ncol=3)
    add_cms_label(ax)
    fig.tight_layout()
    fig.savefig(config["output"], dpi=150)
    plt.close(fig)
    print(f"Wrote {config['output']}")


def build_2d_grid(branches, config):
    x_branch = config["x_branch"]
    y_branch = config["y_branch"]
    for name in (x_branch, y_branch, "deltaNLL"):
        if name not in branches:
            raise RuntimeError(f"Branch {name} not found in {config['input']}")

    start = scan_start_index(branches)
    x_values = as_float_array(branches[x_branch][start:])
    y_values = as_float_array(branches[y_branch][start:])
    q = 2.0 * as_float_array(branches["deltaNLL"][start:])

    mask = np.isfinite(x_values) & np.isfinite(y_values) & np.isfinite(q)
    x_values = x_values[mask]
    y_values = y_values[mask]
    q = q[mask]

    rows = [(round(float(x), 10), round(float(y), 10), float(z)) for x, y, z in zip(x_values, y_values, q)]
    x_vals = sorted(set(x for x, _, _ in rows))
    y_vals = sorted(set(y for _, y, _ in rows))
    nx = len(x_vals)
    ny = len(y_vals)
    expected = nx * ny

    if len(rows) != expected:
        missing = []
        existing = set((x, y) for x, y, _ in rows)
        for x in x_vals:
            for y in y_vals:
                if (x, y) not in existing:
                    missing.append((x, y))
        message = [
            f"ERROR: incomplete 2D grid in {config['input']}",
            f"  finite grid points = {len(rows)}",
            f"  expected grid    = {expected} ({nx} x {ny})",
            f"  missing cells    = {len(missing)}",
        ]
        for x, y in missing[:20]:
            message.append(f"    {x_branch}={x:+.8f}  {y_branch}={y:+.8f}")
        message.append(f"Rerun: {config['rerun']}")
        raise RuntimeError("\n".join(message))

    x_index = {x: i for i, x in enumerate(x_vals)}
    y_index = {y: i for i, y in enumerate(y_vals)}
    z = np.full((ny, nx), np.nan)
    for x, y, value in rows:
        z[y_index[y], x_index[x]] = value

    if np.any(~np.isfinite(z)):
        raise RuntimeError(f"2D grid contains missing or non-finite cells in {config['input']}")

    z = z - np.nanmin(z)
    x_grid, y_grid = np.meshgrid(np.asarray(x_vals), np.asarray(y_vals))
    return x_grid, y_grid, z


def best_fit_point(branches, config):
    x_branch = config["x_branch"]
    y_branch = config["y_branch"]
    if x_branch in branches and y_branch in branches and len(branches[x_branch]) > 0:
        return float(branches[x_branch][0]), float(branches[y_branch][0])
    return 1.0, 0.0


def plot_2d(config, branches):
    x_grid, y_grid, z = build_2d_grid(branches, config)
    best_x, best_y = best_fit_point(branches, config)

    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    vmax = max(CL95_2D, float(np.nanpercentile(z, 95.0)))
    mesh = ax.pcolormesh(x_grid, y_grid, z, shading="auto", cmap="Blues_r", vmin=0.0, vmax=vmax)
    cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
    cbar.set_label(r"$-2\Delta\ln\mathcal{L}$")

    c68 = ax.contour(x_grid, y_grid, z, levels=[CL68_2D], colors=["black"], linewidths=[1.8])
    c95 = ax.contour(x_grid, y_grid, z, levels=[CL95_2D], colors=["black"], linewidths=[1.8], linestyles=["--"])
    ax.clabel(c68, fmt={CL68_2D: "68%"}, inline=True, fontsize=10)
    ax.clabel(c95, fmt={CL95_2D: "95%"}, inline=True, fontsize=10)

    ax.plot(best_x, best_y, marker="+", ms=13, mew=2.2, color="black", zorder=5)
    if config["x_branch"] == "kappa_t" and config["y_branch"] == "kappa_tilde":
        ax.plot(1.0, 0.0, marker="*", ms=14, color="#DAA520", markeredgecolor="black", zorder=5)

    handles = [
        Line2D([0], [0], color="black", lw=1.8, label="68% CL"),
        Line2D([0], [0], color="black", lw=1.8, ls="--", label="95% CL"),
        Line2D([0], [0], marker="+", color="black", lw=0, markersize=11, markeredgewidth=2, label="Best fit"),
        Line2D([0], [0], marker="*", color="#DAA520", markeredgecolor="black", lw=0, markersize=12, label="SM"),
    ]

    ax.set_xlabel(config["x_label"])
    ax.set_ylabel(config["y_label"])
    ax.set_title(config["title"])
    ax.set_xlim(float(np.nanmin(x_grid)), float(np.nanmax(x_grid)))
    ax.set_ylim(float(np.nanmin(y_grid)), float(np.nanmax(y_grid)))
    ax.grid(True, which="major", alpha=0.20)
    ax.legend(handles=handles, loc="upper right", frameon=False)
    add_cms_label(ax)
    fig.tight_layout()
    fig.savefig(config["output"], dpi=150)
    plt.close(fig)
    print(f"Wrote {config['output']}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    apply_cms_matplotlib_style()

    made_any = False
    for config in PLOTS:
        branches = read_tree(config["input"])
        if branches is None:
            continue
        if config["kind"] == "1d":
            plot_1d(config, branches)
        elif config["kind"] == "2d":
            plot_2d(config, branches)
        else:
            raise RuntimeError(f"Unknown plot kind {config['kind']}")
        made_any = True

    if not made_any:
        print("No standard likelihood-scan ROOT files found in outputs/.")
        print("Run:")
        print("  bash scripts/run_limits.sh both massfit")
        print("  bash scripts/run_scan_2d.sh massfit")
        print("  bash scripts/run_limits.sh both cpgg")
        print("  bash scripts/run_scan_2d.sh cpgg")


if __name__ == "__main__":
    main()