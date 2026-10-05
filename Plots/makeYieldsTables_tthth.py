#!/usr/bin/env python3
# Yields / purity table for the ttH+tH CP analysis.
#  * Categories, processes and yields directory are taken from the pipeline
#    definition in run_pipeline_for_final_fits_tth_th.sh (Signal/config_2024.py
#    'cats', Datacard/RunYields.py 'procs' and Datacard/yields_tth_th_cp_Analysis/).
#  * Read in per-category pandas dataframes (pkl) produced by Datacard/RunYields.py

import os
import re
import sys
import glob
import pickle
import json
from optparse import OptionParser
from collections import OrderedDict as od

import pandas as pd

print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP YIELDS TABLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
def leave():
  print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP YIELDS TABLE (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
  exit(0)

# Analysis categories (Signal/config_2024.py: cats), tagged with their base group
# so related categories can be separated visually in the output table.
CP_CATEGORIES = od()
CP_CATEGORIES["tHq_had0_CP_even"] = "tHq_had0"
CP_CATEGORIES["tHq_had0_CP_mix"]  = "tHq_had0"
CP_CATEGORIES["ttH_had0_CP_even"] = "ttH_had0"
CP_CATEGORIES["ttH_had0_CP_odd"]  = "ttH_had0"

# Signal processes produced by the pipeline (Datacard/RunYields.py --procs auto),
# grouped by production mode. A mode with a CP-odd benchmark sample also has a
# CP-even (SM) sample of the same name with no suffix - the pair is what the
# datacard interpolates over an arbitrary CP-mixing angle, so besides the mode
# fraction it's useful to see the CP-odd/CP-even split within that mode too.
PRODUCTION_MODE_PROCS = od()
PRODUCTION_MODE_PROCS["ggH"]     = ["GG2H"]
PRODUCTION_MODE_PROCS["ttH"]     = ["TTH", "tthCPodd"]
# tHqHadKt0Ktt0/tHqHadKtm1Ktt0 (and the lep equivalents) are additional tHq
# anomalous-coupling (kt/ktt) benchmark samples from the same procs list as the
# CP-odd ones (Signal/run_signal_fit.sh) - group them with their production mode.
# PRODUCTION_MODE_PROCS["tHq_had"] = ["tHqHad", "tHqHadCPodd", "tHqHadKt0Ktt0", "tHqHadKtm1Ktt0"]
# PRODUCTION_MODE_PROCS["tHq_lep"] = ["tHqLep", "tHqLepCPodd", "tHqLepKt0Ktt0", "tHqLepKtm1Ktt0"]

PRODUCTION_MODE_PROCS["tHq_had"] = ["tHqHad", "tHqHadCPodd"]#, "tHqHadKt0Ktt0", "tHqHadKtm1Ktt0"]
PRODUCTION_MODE_PROCS["tHq_lep"] = ["tHqLep", "tHqLepCPodd"]#, "tHqLepKt0Ktt0", "tHqLepKtm1Ktt0"]

# CP-even/CP-odd benchmark pair for each mode that has one (mode -> (even proc, odd proc))
CP_BENCHMARK_PROCS = od()
CP_BENCHMARK_PROCS["ttH"]     = ("TTH", "tthCPodd")
CP_BENCHMARK_PROCS["tHq_had"] = ("tHqHad", "tHqHadCPodd")
CP_BENCHMARK_PROCS["tHq_lep"] = ("tHqLep", "tHqLepCPodd")

# Production mode each category is designed to select (drives the "target purity" column)
CATEGORY_TARGET_MODE = od()
for _cat in CP_CATEGORIES:
  if _cat.startswith("ttH_"): CATEGORY_TARGET_MODE[_cat] = "ttH"
  elif "tHq_lep" in _cat: CATEGORY_TARGET_MODE[_cat] = "tHq_lep"
  elif "tHq_had" in _cat: CATEGORY_TARGET_MODE[_cat] = "tHq_had"
  else: CATEGORY_TARGET_MODE[_cat] = None

def get_options():
  parser = OptionParser()
  parser.add_option("--yieldsDir", dest="yieldsDir", default="../Datacard/yields_tth_th_cp_Analysis", help="Directory of per-category yield pkl files (from Datacard/RunYields.py)")
  parser.add_option("--combinedYieldsPkl", dest="combinedYieldsPkl", default='', help="Single combined yields pickle, e.g. Datacard_tth_th_cp_Analysis.pkl (overrides --yieldsDir)")
  parser.add_option("--catInfoPkl", dest="catInfoPkl", default='', help="Load eff sigma, bkg and S/S+B from pickle file (see Plots/getCatInfo.py --saveCatInfo)")
  parser.add_option("--ext", dest="ext", default='', help="Extension for saving, e.g. _tth_th_cp_Analysis")
  parser.add_option("--yieldVar", dest="yieldVar", default='nominal_yield', help="Name of yield column in dataframe")
  # nominal_yield is eff*acc only (no XS*BR, no lumi - see Datacard/makeDatacard.py:102
  # "In HiggsDNA the sumw = eff*acc"). The only place XS*BR*rate actually gets computed
  # in this codebase is makeDatacard.py's --prune block (true_yield = xsbr*ea*rate,
  # Datacard/makeDatacard.py:102-117), and that result is only ever used internally for
  # the pruning decision - never written to any table. --trueYield reproduces that same
  # formula here so it can be, staying as close to makeDatacard.py's own code as possible.
  parser.add_option("--trueYield", dest="trueYield", default=False, action="store_true", help="Scale nominal_yield by XS*BR (Datacard/tools/XSBR.py) and by the per-row 'rate' column (lumi, pb^-1) before summing, i.e. use makeDatacard.py's --prune 'true_yield' formula instead of the raw eff*acc nominal_yield. Output goes to a separate *_trueYield.txt file.")
  parser.add_option("--mass", dest="mass", default='125', help="MH mass, used to look up XS*BR when --trueYield is set")
  parser.add_option("--analysis", dest="analysis", default='tth_th_cp_Analysis', help="Analysis name in Datacard/tools/XSBR.py's XSBRMap, used to look up XS*BR when --trueYield is set")
  parser.add_option("--catLabels", dest="catLabels", default=None, help="JSON mapping category name -> display label (optional, e.g. your own cats_latex.json)")
  parser.add_option("--modeLabels", dest="modeLabels", default=None, help="JSON mapping production-mode name (ggH/ttH/tHq_had/tHq_lep) -> display label (optional)")
  return parser.parse_args()
(opt,args) = get_options()

def EscapeLatex(s):
  # Raw category/mode names (e.g. "tHq_had0_CP_even", "tHq_had") contain "_",
  # which LaTeX reads as a subscript operator outside math mode and errors on.
  return re.sub(r'(?<!\\)_', r'\_', s)
def Translate(name, ndict):
  return EscapeLatex(ndict[name]) if name in ndict else EscapeLatex(name)
def LoadTranslations(jsonfilename):
  with open(jsonfilename) as jsonfile:
    return json.load(jsonfile)
# Both --catLabels/--modeLabels are optional: with neither given, raw category
# and production-mode names (e.g. "ttH_had0_CP_odd", "tHq_had") are printed as-is.
catLabels = {} if opt.catLabels is None else LoadTranslations(opt.catLabels)
modeLabels = {} if opt.modeLabels is None else LoadTranslations(opt.modeLabels)

# Load input dataframe: either one combined pkl, or concatenate every per-category
# pkl found in --yieldsDir (mirrors how Datacard/makeDatacard.py builds the datacard
# from the concatenation of all pkl files in the yields directory)
if opt.combinedYieldsPkl != '':
  if not os.path.exists(opt.combinedYieldsPkl):
    print(" --> [ERROR] Input pickle file does not exist. Leaving")
    leave()
  with open(opt.combinedYieldsPkl, "rb") as fin: yieldsDf = pickle.load(fin)
else:
  pkl_files = sorted(glob.glob(os.path.join(opt.yieldsDir, "*.pkl")))
  if not pkl_files:
    print(" --> [ERROR] No pkl files found in %s. Leaving"%opt.yieldsDir)
    leave()
  perCatFrames = []
  for f in pkl_files:
    with open(f, "rb") as fin: perCatFrames.append(pickle.load(fin))
  yieldsDf = pd.concat(perCatFrames, ignore_index=True)

missingCats = [cat for cat in CP_CATEGORIES if cat not in set(yieldsDf['cat'])]
if missingCats:
  print(" --> [WARNING] No yields found for categories: %s"%", ".join(missingCats))

# --trueYield: reproduce Datacard/makeDatacard.py's --prune true_yield formula
# (true_yield = xsbr * ea * rate, Datacard/makeDatacard.py:102-117) so it can be summed
# into a table like nominal_yield is, instead of only ever being used internally for
# the pruning decision. Kept as close to that code as possible: same column names
# ('xsbr', 'ea', 'true_yield'), same "ea = nominal_yield" ("In HiggsDNA the sumw =
# eff*acc"), same per-row xsbr*ea*rate multiplication before any summing.
yieldVar = opt.yieldVar
if opt.trueYield:
  sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Datacard"))
  from tools.XSBR import extractXSBR

  sigMaskAll = yieldsDf['type']=='sig'
  XSBR = extractXSBR(yieldsDf, mass=opt.mass, analysis=opt.analysis)

  yieldsDf['xsbr'] = '-'
  yieldsDf.loc[sigMaskAll,'xsbr'] = yieldsDf[sigMaskAll].apply(lambda x: XSBR["XS_%s"%x['procOriginal']]*XSBR['BR'], axis=1)

  yieldsDf['ea'] = '-'
  yieldsDf.loc[sigMaskAll,'ea'] = yieldsDf.loc[sigMaskAll,'nominal_yield']

  yieldsDf['true_yield'] = '-'
  yieldsDf.loc[sigMaskAll,'true_yield'] = yieldsDf[sigMaskAll].apply(lambda x: x['xsbr']*x['ea']*x['rate'], axis=1)

  yieldVar = 'true_yield'

# Load cat info dataframe
if opt.catInfoPkl != '':
  if not os.path.exists(opt.catInfoPkl):
    print(" --> [ERROR] Cat info pickle file does not exist. Leaving")
    leave()
  with open(opt.catInfoPkl, "rb") as fin: catInfoDf = pickle.load(fin)

# Initiate pandas dataframe
_columns = ['cat', 'nominal_yield', 'target_mode', 'target_mode_yield']
for mode in PRODUCTION_MODE_PROCS: _columns.append("%s_yield"%mode)
_columns.append('cp_odd_yield')
if opt.catInfoPkl != '': _columns.extend(['effSigma', 'bkg', 'SoverSplusB'])
tableDf = pd.DataFrame(columns=_columns)

# Only processes listed in PRODUCTION_MODE_PROCS count towards Total, so the
# mode-fraction columns always sum to 100% of it.
knownProcs = set(p for procs in PRODUCTION_MODE_PROCS.values() for p in procs)

# Fill frame: sum signal yields (across all years) per category / production mode
for cat in CP_CATEGORIES:
  sigMask = (yieldsDf['cat']==cat)&(yieldsDf['type']=='sig')
  if not sigMask.any():
    continue

  # Guard against a new signal sample being added to the pipeline without this
  # script's grouping being updated - it would otherwise be silently dropped
  # from both the Total and the mode fractions.
  unclassified = set(yieldsDf[sigMask]['procOriginal'].unique()) - knownProcs
  if unclassified:
    print(" --> [WARNING] %s: unclassified signal processes not in any PRODUCTION_MODE_PROCS group, excluded from Total: %s"%(cat, ", ".join(sorted(unclassified))))

  knownMask = sigMask & yieldsDf['procOriginal'].isin(knownProcs)
  catYield = yieldsDf[knownMask][yieldVar].sum()
  targetMode = CATEGORY_TARGET_MODE[cat]

  modeYields = od()
  for mode, procs in PRODUCTION_MODE_PROCS.items():
    modeYields[mode] = yieldsDf[sigMask & yieldsDf['procOriginal'].isin(procs)][yieldVar].sum()

  targetModeYield = modeYields[targetMode] if targetMode is not None else 0.

  # CP-odd fraction within the category's target mode (its own benchmark pair)
  cpOddYield = 0.
  if targetMode in CP_BENCHMARK_PROCS:
    _, oddProc = CP_BENCHMARK_PROCS[targetMode]
    cpOddYield = yieldsDf[sigMask & (yieldsDf['procOriginal']==oddProc)][yieldVar].sum()

  if opt.catInfoPkl != '':
    catInfoMask = catInfoDf['cat']==cat
    effSigma = catInfoDf[catInfoMask]['effSigma'].values[0]
    bkgPerGeV = catInfoDf[catInfoMask]['bkg_per_GeV'].values[0]
    sOverSplusB = catInfoDf[catInfoMask]['SoverSplusB'].values[0]

  # Add values to dataframe
  vals = [cat, catYield, targetMode, targetModeYield]
  for mode in PRODUCTION_MODE_PROCS: vals.append(modeYields[mode])
  vals.append(cpOddYield)
  if opt.catInfoPkl != '': vals.extend([effSigma,bkgPerGeV,sOverSplusB])
  tableDf.loc[len(tableDf)] = vals

if len(tableDf) == 0:
  print(" --> [ERROR] No categories with signal yields found. Leaving")
  leave()

# Make table: cat, total, target-mode purity, [mode fraction]*, CP-odd(target), [effSigma, S/S+B]
os.makedirs("Tables", exist_ok=True)
nColumns = 4 + len(PRODUCTION_MODE_PROCS)
if opt.catInfoPkl != '': nColumns += 2
outSuffix = "_trueYield" if opt.trueYield else ""
fout = open("Tables/yields_table_lite_tthth%s%s.txt"%(opt.ext,outSuffix),"w")
fout.write("\\begin{tabular}{%s}\n"%("l|"+("c"*(nColumns-1))))
fout.write("    \\multirow{3}{*}{Analysis categories} & \\multicolumn{%g}{c}{ttH+tH CP analysis expected signal} \\\\ \n"%(nColumns-1))
modeHeader = " & ".join(Translate(mode,modeLabels) for mode in PRODUCTION_MODE_PROCS)
tailCols = " & \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}$\\sigma_{\\rm{eff}}$\\\\(GeV)\\end{tabular}} & \\multirow{2}{*}{S/(S+B)}" if opt.catInfoPkl != '' else ""
fout.write("     & \\multirow{2}{*}{Total} & \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}Target\\\\mode\\end{tabular}} & \\multicolumn{%g}{c}{Production Mode Fractions} & \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}CP-odd\\\\(target)\\end{tabular}}%s \\\\ \n"%(len(PRODUCTION_MODE_PROCS),tailCols))
fout.write("     & & & %s &%s \\\\ \\hline \n"%(modeHeader, " &" if opt.catInfoPkl != '' else ""))

# Add rows, separating the tHq_had0 and ttH_had0 blocks with a \cmsTabSkip
rows = list(tableDf.iterrows())
for idx, (ir,r) in enumerate(rows):
  group = CP_CATEGORIES[r['cat']]
  nextGroup = CP_CATEGORIES[rows[idx+1][1]['cat']] if idx+1 < len(rows) else None

  targetPct = 100*(r['target_mode_yield']/r['nominal_yield']) if r['nominal_yield'] else 0.
  catLine = "     %s & %.4f & %.1f\\%%"%(Translate(r['cat'],catLabels),r['nominal_yield'],targetPct)
  for mode in PRODUCTION_MODE_PROCS:
    modePct = 100*(r['%s_yield'%mode]/r['nominal_yield']) if r['nominal_yield'] else 0.
    catLine += " & -" if modePct <= 0. else " & %.1f\\%%"%modePct
  catLine += " & %.1f\\%%"%(100*(r['cp_odd_yield']/r['target_mode_yield'])) if r['target_mode_yield'] else " & -"
  if opt.catInfoPkl != '':
    catLine += " & %.2f & %.2f"%(r['effSigma'],r['SoverSplusB'])
  fout.write("%s \\\\ \n"%catLine)
  if nextGroup != group: fout.write("     [\\cmsTabSkip]\n")

fout.write("\\end{tabular}\n")
fout.close()
print(" --> Saved: Tables/yields_table_lite_tthth%s%s.txt"%(opt.ext,outSuffix))
leave()
