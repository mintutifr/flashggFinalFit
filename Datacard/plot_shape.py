#!/usr/bin/env python3
"""
script to roduce the standard mass-fit input diagnostic plots.
"""

import math
import os
import sys

try:
    import ROOT
except ImportError:
    sys.exit("Error no pyroot. Run inside a ROOT/CMSSW env.")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_FILE = os.path.join(BASE_DIR, "Signal", "outdir_packaged", "CMS-HGG_sigfit_packaged_ttH_had0_CP_odd.root")

DATACARD_FILE = os.path.join(SCRIPT_DIR, "Datacard_tth_th_cp_Analysis.txt")

# OUTPUT_DIR = os.path.join(SCRIPT_DIR, "outputs", "rates_1")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "outputs", "rates_1_bin_32")


def apply_cms_root_style():
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetTitleFillColor(0)
    ROOT.gStyle.SetFrameLineWidth(2)
    ROOT.gStyle.SetLineWidth(2)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)


def draw_cms_label():
    label = ROOT.TLatex()
    label.SetNDC(True)
    label.SetTextFont(61)
    label.SetTextSize(0.052)
    label.DrawLatex(0.14, 0.93, "CMS")
    label.SetTextFont(52)
    label.SetTextSize(0.040)
    label.DrawLatex(0.24, 0.93, "Private")
    label.SetTextFont(42)
    label.SetTextSize(0.038)
    label.SetTextAlign(31)
    label.DrawLatex(0.96, 0.93, "13 TeV")
    label.SetTextAlign(11)
    return label

def get_workspace(filename, ws_name="wsig_13TeV"):
    root_file = ROOT.TFile.Open(filename)
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"Could not open file: {filename}")
    workspace = root_file.Get(ws_name)
    if not workspace:
        raise RuntimeError(f"Workspace '{ws_name}' not found in {filename}")
    return root_file, workspace


def main():
    ROOT.gROOT.SetBatch(True)
    apply_cms_root_style()
    ROOT.TH1.SetDefaultSumw2(True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    root_file, workspace = get_workspace(INPUT_FILE)
    #mass = workspace.var("mass")
    mass = workspace.var("CMS_hgg_mass")
    print(f"Mass variable: {mass}")
    if not mass:
        raise RuntimeError("No 'CMS_hgg_mass' in workspace")

    # The signal pdf's mean/sigma are RooSpline1D interpolations vs MH, so the
    # plotted peak sits wherever MH currently is in the workspace unless pinned
    # here (mirrors Signal/RunPlotter.py's w.var("MH").setVal(...) before plotting).
    mh = workspace.var("MH")
    if not mh:
        raise RuntimeError("No 'MH' in workspace")
    mh.setVal(125)
    print(f"MH set to: {mh.getVal()}")

    for v in workspace.allVars():
        name = v.GetName()
        print(f"{name:100s} = {v.getVal():.6f}")
  
    # pdf_name = "hggpdfsmrel_TTH_2022preEE_ttH_had0_CP_even_13TeV"
    # pdf_name = "hggpdfsmrel_tthCPodd_2022preEE_ttH_had0_CP_even_13TeV"
    pdf_name = "hggpdfsmrel_tthCPodd_2024_ttH_had0_CP_odd_13TeV"


    parent_pdf = workspace.pdf(pdf_name)

    print("pdf Class:", parent_pdf.ClassName())

    pdfs = parent_pdf.pdfList()
    coeffs = parent_pdf.coefList()

    for i in range(pdfs.getSize()):
        component = pdfs.at(i)
        coefficient = coeffs.at(i)

        print(f"Component {i}: {component.GetName()}, Coefficient: {coefficient.GetName()}", "Value:", coefficient.getVal())

    extend = ["extendhggpdfsmrel_tthCPodd_2024_ttH_had0_CP_odd_13TeV",
                "extendhggpdfsmrel_tthCPodd_2024_ttH_had0_CP_odd_13TeVThisLumi"]

    pdf = parent_pdf

    if not pdf:
        raise RuntimeError(f"PDF {pdf_name} not found")

    frame = mass.frame(
        # ROOT.RooFit.Title("ttH 2022preEE CP-even"),
        # ROOT.RooFit.Title("ttH 2022preEE CP-odd"),
        ROOT.RooFit.Title("ttH 2024 CP-odd (cat: ttH_had0_CP_odd)"),
        ROOT.RooFit.Bins(80)
    )

    pdf.plotOn(
        frame,
        ROOT.RooFit.LineWidth(2)
    )

    c = ROOT.TCanvas("c", "c", 800, 600)
    frame.Draw()
    c.SaveAs(f"{OUTPUT_DIR}/ttH_2024_CP_odd_cat_ttH_had0_CP_odd.pdf")


if __name__ == "__main__":
    main()

