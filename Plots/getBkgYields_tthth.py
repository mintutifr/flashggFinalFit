#!/usr/bin/env python3
# Background (observed data) event counts for the ttH+tH CP analysis categories.
#  * Reads the fitted background workspace per category
#    (Background/outdir_tth_th_cp_Analysis/CMS-HGG_multipdf_<cat>.root, produced by
#    Background/run_Background_fit.sh) and sums roohist_data_mass_<cat>.
#  * No MC truth exists for background (Datacard/makeYields.py never fills a
#    real nominal_yield for type=='bkg' rows - see Datacard/makeYields.py:131-161),
#    so this counts the observed data the background shape was fit to instead.
#  * Default: the blind window is excluded (sideband only), matching the blinding
#    used when the background shape itself was fit (Background/test/fTest.cpp).
#  * --unblind: count every entry, including the blind window.
#
# Usable standalone (writes Tables/bkg_events_table<ext>.txt) or imported, e.g.
# from getBkgYields_tthth import getBkgYields

import os
import re
import glob
import pickle
from optparse import OptionParser

import ROOT
import pandas as pd

ROOT.gROOT.SetBatch(True)

print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP BACKGROUND EVENTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
def leave():
  print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP BACKGROUND EVENTS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
  exit(0)

def get_options():
  parser = OptionParser()
  parser.add_option("--bkgWSDir", dest="bkgWSDir", default="../Background/outdir_tth_th_cp_Analysis", help="Directory of fitted background workspaces (CMS-HGG_multipdf_<cat>.root), from Background/run_Background_fit.sh")
  parser.add_option("--bkgWSName", dest="bkgWSName", default="multipdf", help="Name of the RooWorkspace object inside each file")
  parser.add_option("--cats", dest="cats", default="auto", help="Comma separated list of categories. auto = every CMS-HGG_multipdf_*.root found in --bkgWSDir")
  parser.add_option("--blindWindow", dest="blindWindow", default="115,135", help="Signal mass window excluded by default: low,high. Pass '' to disable")
  parser.add_option("--unblind", dest="unblind", default=False, action="store_true", help="Count every data event, including the blind window (default: blind window excluded)")
  parser.add_option("--ext", dest="ext", default="_tth_th_cp_Analysis", help="Extension for saving, e.g. _tth_th_cp_Analysis")
  parser.add_option("--out", dest="out", default=None, help="Also write the table to this txt file (default: Tables/bkg_events_table<ext>[_unblind].txt)")
  parser.add_option("--savePkl", dest="savePkl", default=None, help="Also save the per-category counts to this pkl file (DataFrame with columns cat,bkg_events,blinded)")
  return parser.parse_args()

def getCatsFromDir(wsDir):
  cats = []
  for f in sorted(glob.glob(os.path.join(wsDir, "CMS-HGG_multipdf_*.root"))):
    m = re.match(r"CMS-HGG_multipdf_(.+)\.root$", os.path.basename(f))
    if m: cats.append(m.group(1))
  return cats

def getBkgDataCount(cat, bkgWSDir, bkgWSName, blindLow, blindHigh, unblind):
  # Returns None (with a printed warning) if the background fit for this
  # category hasn't been run yet (Background/run_Background_fit.sh), so
  # callers can degrade gracefully instead of crashing.
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
  dataName = "roohist_data_mass_%s"%cat
  dh = w.data(dataName)
  if not dh:
    print(" --> [WARNING] %s: dataset '%s' not found in workspace"%(cat,dataName))
    f.Close()
    return None
  if unblind or blindLow is None:
    n = dh.sumEntries()
  else:
    xvarName = dh.get().first().GetName()
    n = dh.sumEntries("%s<%g||%s>%g"%(xvarName,blindLow,xvarName,blindHigh))
  f.Close()
  return n

def getBkgYields(cats, bkgWSDir="../Background/outdir_tth_th_cp_Analysis", bkgWSName="multipdf", blindWindow="115,135", unblind=False):
  # Returns an {cat: count-or-None} dict. count is the observed data yield
  # (sideband-only unless unblind=True); None means the category's background
  # workspace wasn't found.
  blindLow, blindHigh = None, None
  if blindWindow:
    blindLow, blindHigh = [float(x) for x in blindWindow.split(",")]
  return {cat: getBkgDataCount(cat,bkgWSDir,bkgWSName,blindLow,blindHigh,unblind) for cat in cats}

if __name__ == "__main__":
  (opt,args) = get_options()

  cats = getCatsFromDir(opt.bkgWSDir) if opt.cats == "auto" else opt.cats.split(",")
  if not cats:
    print(" --> [ERROR] No categories found in %s. Leaving"%opt.bkgWSDir)
    leave()

  bkgYields = getBkgYields(cats, opt.bkgWSDir, opt.bkgWSName, opt.blindWindow, opt.unblind)

  df = pd.DataFrame([[cat, bkgYields[cat]] for cat in cats], columns=["cat","bkg_events"])

  pd.set_option("display.max_columns", None)
  pd.set_option("display.width", 1000)

  blindLow, blindHigh = [float(x) for x in opt.blindWindow.split(",")] if opt.blindWindow else (None,None)
  windowDesc = "unblinded (full mass range)" if opt.unblind else ("blind window [%g,%g] excluded"%(blindLow,blindHigh) if blindLow is not None else "no blind window set")

  lines = [" -- Background (observed data) events per category: %s --"%windowDesc, df.to_string(index=False)]
  out = "\n".join(lines)
  print(out)

  os.makedirs("Tables", exist_ok=True)
  outPath = opt.out if opt.out else "Tables/bkg_events_table%s%s.txt"%(opt.ext, "_unblind" if opt.unblind else "")
  with open(outPath,"w") as fo: fo.write(out+"\n")
  print(" --> Saved: %s"%outPath)

  if opt.savePkl:
    df["blinded"] = not opt.unblind
    with open(opt.savePkl,"wb") as fp: pickle.dump(df, fp)
    print(" --> Saved: %s"%opt.savePkl)

  leave()
