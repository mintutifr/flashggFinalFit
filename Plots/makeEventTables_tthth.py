#!/usr/bin/env python3
# Raw MC event-count / purity table for the ttH+tH CP analysis - same category and
# production-mode breakdown as makeYieldsTables_tthth.py, but summing the raw
# (unweighted) number of simulated events per process (numEntries) instead of the
# weighted nominal_yield.
#  * Categories, processes and yields directory are taken from the pipeline
#    definition in run_pipeline_for_final_fits_tth_th.sh (Signal/config_2024.py
#    'cats', Datacard/RunYields.py 'procs' and Datacard/yields_tth_th_cp_Analysis/).
#  * Read in per-category text files (numEntries, nominal_yield) produced by
#    Datacard/count_mc_events.py (run via Datacard/run_count_mc_events.sh) - these
#    are not stored in the yields pkl itself, since RunYields.py never records the
#    raw event count, only the weighted sum (nominal_yield).

import os
import re
import glob
import json
from optparse import OptionParser
from collections import OrderedDict as od

import pandas as pd

print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP EVENT COUNT TABLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
def leave():
  print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ttH/tH CP EVENT COUNT TABLE (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
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
# tHqHadKt0Ktt0/tHqHadKtm1Ktt0 (and the lep equivalents) are additional tHq
# anomalous-coupling (kt/ktt) benchmark samples, deliberately excluded here (kept
# in sync with Plots/makeYieldsTables_tthth.py) so Total only covers processes
# classified into a production mode and the mode-fraction columns sum to 100%.
PRODUCTION_MODE_PROCS = od()
PRODUCTION_MODE_PROCS["ggH"]     = ["GG2H"]
PRODUCTION_MODE_PROCS["ttH"]     = ["TTH", "tthCPodd"]
PRODUCTION_MODE_PROCS["tHq_had"] = ["tHqHad", "tHqHadCPodd"]
PRODUCTION_MODE_PROCS["tHq_lep"] = ["tHqLep", "tHqLepCPodd"]

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
  parser.add_option("--yieldsDir", dest="yieldsDir", default="../Datacard/yields_tth_th_cp_Analysis", help="Directory of per-category *_numEvents.txt files (from Datacard/count_mc_events.py)")
  parser.add_option("--ext", dest="ext", default='', help="Extension for saving, e.g. _tth_th_cp_Analysis")
  parser.add_option("--yieldVar", dest="yieldVar", default='numEntries', help="Name of column in the *_numEvents.txt files to sum (numEntries or nominal_yield)")
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

# Load input dataframe: concatenate every per-category *_numEvents.txt found in
# --yieldsDir (produced by Datacard/count_mc_events.py, one file per category)
txt_files = sorted(glob.glob(os.path.join(opt.yieldsDir, "*_numEvents.txt")))
if not txt_files:
  print(" --> [ERROR] No *_numEvents.txt files found in %s. Run Datacard/run_count_mc_events.sh first. Leaving"%opt.yieldsDir)
  leave()
perCatFrames = [pd.read_csv(f, sep=r"\s+", engine="python") for f in txt_files]
yieldsDf = pd.concat(perCatFrames, ignore_index=True)

missingCats = [cat for cat in CP_CATEGORIES if cat not in set(yieldsDf['cat'])]
if missingCats:
  print(" --> [WARNING] No event counts found for categories: %s"%", ".join(missingCats))

# Initiate pandas dataframe
_columns = ['cat', 'nominal_yield', 'target_mode', 'target_mode_yield']
for mode in PRODUCTION_MODE_PROCS: _columns.append("%s_yield"%mode)
_columns.append('cp_odd_yield')
tableDf = pd.DataFrame(columns=_columns)

# Only processes listed in PRODUCTION_MODE_PROCS count towards Total, so the
# mode-fraction columns always sum to 100% of it.
knownProcs = set(p for procs in PRODUCTION_MODE_PROCS.values() for p in procs)

# Fill frame: sum event counts (across all years) per category / production mode
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
  catYield = yieldsDf[knownMask][opt.yieldVar].sum()
  targetMode = CATEGORY_TARGET_MODE[cat]

  modeYields = od()
  for mode, procs in PRODUCTION_MODE_PROCS.items():
    modeYields[mode] = yieldsDf[sigMask & yieldsDf['procOriginal'].isin(procs)][opt.yieldVar].sum()

  targetModeYield = modeYields[targetMode] if targetMode is not None else 0.

  # CP-odd fraction within the category's target mode (its own benchmark pair)
  cpOddYield = 0.
  if targetMode in CP_BENCHMARK_PROCS:
    _, oddProc = CP_BENCHMARK_PROCS[targetMode]
    cpOddYield = yieldsDf[sigMask & (yieldsDf['procOriginal']==oddProc)][opt.yieldVar].sum()

  # Add values to dataframe
  vals = [cat, catYield, targetMode, targetModeYield]
  for mode in PRODUCTION_MODE_PROCS: vals.append(modeYields[mode])
  vals.append(cpOddYield)
  tableDf.loc[len(tableDf)] = vals

if len(tableDf) == 0:
  print(" --> [ERROR] No categories with event counts found. Leaving")
  leave()

# Make table: cat, total, target-mode purity, [mode fraction]*, CP-odd(target)
os.makedirs("Tables", exist_ok=True)
nColumns = 4 + len(PRODUCTION_MODE_PROCS)
fout = open("Tables/event_table_lite_tthth%s.txt"%opt.ext,"w")
fout.write("\\begin{tabular}{%s}\n"%("l|"+("c"*(nColumns-1))))
fout.write("    \\multirow{3}{*}{Analysis categories} & \\multicolumn{%g}{c}{ttH+tH CP analysis MC event counts} \\\\ \n"%(nColumns-1))
modeHeader = " & ".join(Translate(mode,modeLabels) for mode in PRODUCTION_MODE_PROCS)
fout.write("     & \\multirow{2}{*}{Total} & \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}Target\\\\mode\\end{tabular}} & \\multicolumn{%g}{c}{Production Mode Fractions} & \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}CP-odd\\\\(target)\\end{tabular}} \\\\ \n"%len(PRODUCTION_MODE_PROCS))
fout.write("     & & & %s & \\\\ \\hline \n"%modeHeader)

# Add rows, separating the tHq_had0 and ttH_had0 blocks with a \cmsTabSkip
rows = list(tableDf.iterrows())
for idx, (ir,r) in enumerate(rows):
  group = CP_CATEGORIES[r['cat']]
  nextGroup = CP_CATEGORIES[rows[idx+1][1]['cat']] if idx+1 < len(rows) else None

  targetPct = 100*(r['target_mode_yield']/r['nominal_yield']) if r['nominal_yield'] else 0.
  catLine = "     %s & %d & %.1f\\%%"%(Translate(r['cat'],catLabels),r['nominal_yield'],targetPct)
  for mode in PRODUCTION_MODE_PROCS:
    modePct = 100*(r['%s_yield'%mode]/r['nominal_yield']) if r['nominal_yield'] else 0.
    catLine += " & -" if modePct <= 0. else " & %.1f\\%%"%modePct
  catLine += " & %.1f\\%%"%(100*(r['cp_odd_yield']/r['target_mode_yield'])) if r['target_mode_yield'] else " & -"
  fout.write("%s \\\\ \n"%catLine)
  if nextGroup != group: fout.write("     [\\cmsTabSkip]\n")

fout.write("\\end{tabular}\n")
fout.close()
print(" --> Saved: Tables/event_table_lite_tthth%s.txt"%opt.ext)
leave()
