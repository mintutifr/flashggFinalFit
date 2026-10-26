#!/usr/bin/env python3
# Expected background yield at a fixed mass point, from the best-fit background
# shape chosen by the F-test (Background/run_Background_fit.sh).
#  * Reads the same fitted RooMultiPdf workspace as getBkgYields_tthth.py
#    (Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_<cat>.root).
#  * RooMultiPdf::getVal() automatically dispatches to whichever sub-pdf its
#    pdfindex category currently points to (the winning family from the F-test,
#    already fit and saved in the workspace) - so no manual index bookkeeping
#    is needed here.
#  * Returns density [events/GeV] x normalization [events] = the expected
#    number of background events per GeV at --mass (default 125.09 GeV).
#
# Usable standalone (writes Tables/expected_bkg_yield_table<ext>.txt) or
# imported, e.g. from expected_bkg_yield import getExpectedBkgYields

import os
import re
import glob
import pickle
from optparse import OptionParser

import ROOT
import pandas as pd

ROOT.gROOT.SetBatch(True)

print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP EXPECTED BACKGROUND YIELD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
def leave():
  print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP EXPECTED BACKGROUND YIELD (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
  exit(0)

def get_options():
  parser = OptionParser()
  parser.add_option("--bkgWSDir", dest="bkgWSDir", default="../Background/outdir_tth_th_cp_Analysis", help="Directory of fitted background workspaces (CMS-HGG_multipdf_<cat>.root), from Background/run_Background_fit.sh")
  parser.add_option("--bkgWSName", dest="bkgWSName", default="multipdf", help="Name of the RooWorkspace object inside each file")
  parser.add_option("--cats", dest="cats", default="auto", help="Comma separated list of categories. auto = every CMS-HGG_multipdf_*.root found in --bkgWSDir")
  parser.add_option("--mass", dest="mass", default=125.09, type="float", help="Mass point [GeV] to evaluate the background shape at (default: 125.09)")
  parser.add_option("--ext", dest="ext", default="_tth_th_cp_Analysis", help="Extension for saving, e.g. _tth_th_cp_Analysis")
  parser.add_option("--out", dest="out", default=None, help="Also write the table to this txt file (default: Tables/expected_bkg_yield_table<ext>.txt)")
  parser.add_option("--savePkl", dest="savePkl", default=None, help="Also save the per-category values to this pkl file (DataFrame with columns cat,expected_bkg_yield,mass)")
  return parser.parse_args()

def getCatsFromDir(wsDir):
  cats = []
  for f in sorted(glob.glob(os.path.join(wsDir, "CMS-HGG_multipdf_*.root"))):
    m = re.match(r"CMS-HGG_multipdf_(.+)\.root$", os.path.basename(f))
    if m: cats.append(m.group(1))
  return cats

def getExpectedBkgYield(cat, bkgWSDir, bkgWSName, mass):
  # Returns the expected background density [events/GeV] at `mass`, from the
  # winning background-shape family (RooMultiPdf dispatches to its current
  # pdfindex automatically - that index was fixed by the F-test and is already
  # saved in the workspace) times its fitted normalization. None (with a
  # printed warning) if this category's background fit hasn't been run yet.
  fname = os.path.join(bkgWSDir, "CMS-HGG_multipdf_%s.root"%cat)
  if not os.path.exists(fname):
    print(" --> [WARNING] %s: background workspace not found (%s)"%(cat,fname))
    return None
  f = ROOT.TFile.Open(fname)
  if (not f) or f.IsZombie():
    print(" --> [WARNING] %s: could not open %s"%(cat,fname))
    return None
  w = f.Get(bkgWSName)
  if not w:
    print(" --> [WARNING] %s: workspace '%s' not found in %s"%(cat,bkgWSName,fname))
    f.Close()
    return None
  mpdfName = "CMS_hgg_%s_13TeV_bkgshape"%cat
  mpdf = w.pdf(mpdfName)
  if not mpdf:
    print(" --> [WARNING] %s: multipdf '%s' not found in workspace"%(cat,mpdfName))
    f.Close()
    return None
  norm = w.var("%s_norm"%mpdfName)
  if not norm:
    print(" --> [WARNING] %s: normalization '%s_norm' not found in workspace"%(cat,mpdfName))
    f.Close()
    return None
  massVar = w.var("CMS_hgg_mass")
  if not massVar:
    print(" --> [WARNING] %s: observable 'CMS_hgg_mass' not found in workspace"%cat)
    f.Close()
    return None
  massVar.setVal(mass)
  density = mpdf.getVal(ROOT.RooArgSet(massVar))
  expectedYield = density*norm.getVal()
  f.Close()
  return expectedYield

def getExpectedBkgYields(cats, bkgWSDir="../Background/outdir_tth_th_cp_Analysis", bkgWSName="multipdf", mass=125.09):
  # Returns an {cat: value-or-None} dict, see getExpectedBkgYield.
  return {cat: getExpectedBkgYield(cat,bkgWSDir,bkgWSName,mass) for cat in cats}

if __name__ == "__main__":
  (opt,args) = get_options()

  cats = getCatsFromDir(opt.bkgWSDir) if opt.cats == "auto" else opt.cats.split(",")
  if not cats:
    print(" --> [ERROR] No categories found in %s. Leaving"%opt.bkgWSDir)
    leave()

  expectedYields = getExpectedBkgYields(cats, opt.bkgWSDir, opt.bkgWSName, opt.mass)

  df = pd.DataFrame([[cat, expectedYields[cat]] for cat in cats], columns=["cat","expected_bkg_yield"])

  pd.set_option("display.max_columns", None)
  pd.set_option("display.width", 1000)

  lines = [" -- Expected background yield [events/GeV] at m_gg = %.2f GeV, from the best-fit background shape --"%opt.mass, df.to_string(index=False)]
  out = "\n".join(lines)
  print(out)

  os.makedirs("Tables", exist_ok=True)
  outPath = opt.out if opt.out else "Tables/expected_bkg_yield_table%s.txt"%opt.ext
  with open(outPath,"w") as fo: fo.write(out+"\n")
  print(" --> Saved: %s"%outPath)

  if opt.savePkl:
    df["mass"] = opt.mass
    with open(opt.savePkl,"wb") as fp: pickle.dump(df, fp)
    print(" --> Saved: %s"%opt.savePkl)

  leave()
