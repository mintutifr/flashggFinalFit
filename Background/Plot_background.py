#!/usr/bin/env python3
# Plot the observed m_gg spectrum ("background shape") per category, read
# directly from the merged (all years combined) data workspace -- the same
# dataset the background fit (bin/fTest) is run on. With --cat, plots one
# category; without it, overlays every category in --cats on one canvas.

import os
import fnmatch
from optparse import OptionParser
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

DEFAULT_INPUT = "/eos/home-m/mikumar/Final_fits/outputForFinalFits_29Oct2026/root/Data/ws/allData.root"
DEFAULT_CATS = "ttH_had0_CP_even,ttH_had0_CP_odd"
COLORS = [ROOT.kBlack, ROOT.kRed+1, ROOT.kAzure+2, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kMagenta+1, ROOT.kCyan+2, ROOT.kGray+2]


def get_options():
  parser = OptionParser()
  parser.add_option("--input", dest="input", default=DEFAULT_INPUT, help="Input data workspace file, all years combined (default: %s)"%DEFAULT_INPUT)
  parser.add_option("--cat", dest="cat", default=None, help="Single category to plot, a glob pattern (e.g. 'ttH_had0_*') to match several, or 'all' for every category found in the input file. If not given, overlay every category in --cats on one canvas")
  parser.add_option("--cats", dest="cats", default=DEFAULT_CATS, help="Comma separated categories to use when --cat is not given (default: %s)"%DEFAULT_CATS)
  parser.add_option("--xvar", dest="xvar", default="CMS_hgg_mass", help="Observable name in the workspace")
  parser.add_option("--massRange", dest="massRange", default="100,180", help="Mass range to plot: low,high")
  parser.add_option("--nBins", dest="nBins", default=80, type="int", help="Number of bins")
  parser.add_option("--blindWindow", dest="blindWindow", default="115,135", help="Signal mass window to skip (blind): low,high. Pass '' to disable")
  parser.add_option("--outdir", dest="outdir", default="plots_background", help="Output directory for the plot(s)")
  parser.add_option("--ext", dest="ext", default="", help="Extra suffix to add to the output filename")
  return parser.parse_args()
(opt, args) = get_options()


def get_workspace(fname):
  f = ROOT.TFile.Open(fname)
  if (not f) or f.IsZombie():
    raise RuntimeError("Cannot open input file: %s"%fname)
  d = f.Get("tagsDumper")
  if not d:
    raise RuntimeError("tagsDumper directory not found in %s"%fname)
  w = d.Get("cms_hgg_13TeV")
  if not w:
    raise RuntimeError("Workspace cms_hgg_13TeV not found in %s"%fname)
  return f, w


def discover_categories(w):
  prefix = "Data_13TeV_"
  return sorted(d.GetName()[len(prefix):] for d in w.allData() if d.GetName().startswith(prefix))


def get_data_graph(w, cat, xvar, mlow, mhigh, nbins, blind):
  dname = "Data_13TeV_%s"%cat
  data = w.data(dname)
  if not data:
    available = sorted(d.GetName() for d in w.allData())
    raise RuntimeError("Dataset %s not found in workspace. Available: %s"%(dname, available))
  mass = w.var(xvar)
  if not mass:
    raise RuntimeError("Observable %s not found in workspace"%xvar)
  h = data.createHistogram("h_data_%s"%cat, mass, ROOT.RooFit.Binning(nbins, mlow, mhigh))

  # Build a graph from the histogram, skipping bins inside the blind window
  # entirely (not just zeroing them) so no point is drawn there.
  g = ROOT.TGraphErrors()
  g.SetName("g_data_%s"%cat)
  ip = 0
  hmax = 0.
  nEvents, nEventsTotal = 0., 0.
  for b in range(1, h.GetNbinsX()+1):
    x = h.GetBinCenter(b)
    y = h.GetBinContent(b)
    nEventsTotal += y
    if blind and blind[0] <= x <= blind[1]:
      continue
    nEvents += y
    g.SetPoint(ip, x, y)
    g.SetPointError(ip, h.GetBinWidth(b)/2., h.GetBinError(b))
    hmax = max(hmax, y)
    ip += 1
  return g, hmax, nEvents, nEventsTotal


def plot(graphs, hmaxes, cats, mlow, mhigh, nbins, blind, outpath):
  can = ROOT.TCanvas("c", "c", 700, 600)
  leg = ROOT.TLegend(0.60, 0.68, 0.88, 0.88)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetTextFont(42)

  hmax = max(hmaxes)
  axes = ROOT.TH1F("axes", "", nbins, mlow, mhigh)
  axes.SetMaximum(1.35*hmax if hmax > 0 else 1.)
  axes.SetMinimum(0.)
  axes.GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
  axes.GetYaxis().SetTitle("Events / %.2f GeV"%((mhigh-mlow)/nbins))
  axes.Draw("axis")

  if len(cats) > 12:
    leg.SetNColumns(2)

  for i, (cat, g) in enumerate(zip(cats, graphs)):
    col = COLORS[i % len(COLORS)]
    g.SetLineColor(col)
    g.SetMarkerColor(col)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.8)
    g.SetLineWidth(2)
    g.Draw("PE same")
    leg.AddEntry(g, cat, "lep")

  if blind:
    box = ROOT.TBox(blind[0], axes.GetMinimum(), blind[1], axes.GetMaximum())
    box.SetFillColorAlpha(ROOT.kGray, 0.35)
    box.SetLineWidth(0)
    box.Draw("same")
    axes.Draw("axis same")

  leg.Draw()

  lat = ROOT.TLatex()
  lat.SetNDC()
  lat.SetTextFont(42)
  lat.SetTextSize(0.035)
  lat.DrawLatex(0.12, 0.91, "CMS Preliminary")

  for ext in ("png", "pdf"):
    can.SaveAs("%s.%s"%(outpath, ext))
  print("Wrote %s.png"%outpath)


def main():
  mlow, mhigh = [float(x) for x in opt.massRange.split(",")]
  blind = [float(x) for x in opt.blindWindow.split(",")] if opt.blindWindow else None
  os.makedirs(opt.outdir, exist_ok=True)

  f, w = get_workspace(opt.input)

  if opt.cat and opt.cat.lower() == "all":
    cats = discover_categories(w)
  elif opt.cat and any(ch in opt.cat for ch in "*?["):
    cats = [c for c in discover_categories(w) if fnmatch.fnmatch(c, opt.cat)]
    if not cats:
      raise RuntimeError("No category matches pattern %r. Available: %s"%(opt.cat, discover_categories(w)))
  elif opt.cat:
    cats = [opt.cat]
  else:
    cats = [c.strip() for c in opt.cats.split(",") if c.strip()]
  graphs, hmaxes, nEventsList, nEventsTotalList = zip(*[get_data_graph(w, cat, opt.xvar, mlow, mhigh, opt.nBins, blind) for cat in cats])

  windowDesc = "blind window [%g,%g] excluded"%(blind[0],blind[1]) if blind else "no blind window"
  print(" --> Events per category (%s):"%windowDesc)
  for cat, nEvents, nEventsTotal in zip(cats, nEventsList, nEventsTotalList):
    if blind: print("       %-20s  %8.1f   (%.1f including blind window)"%(cat, nEvents, nEventsTotal))
    else: print("       %-20s  %8.1f"%(cat, nEvents))
  if len(cats) > 1:
    if blind: print("       %-20s  %8.1f   (%.1f including blind window)"%("Total", sum(nEventsList), sum(nEventsTotalList)))
    else: print("       %-20s  %8.1f"%("Total", sum(nEventsList)))

  safe_cat = opt.cat.translate(str.maketrans("*?[]", "____")) if opt.cat else None
  suffix = ("_%s"%safe_cat) if safe_cat else "_allCats"
  if opt.ext:
    suffix += "_%s"%opt.ext
  outpath = os.path.join(opt.outdir, "background_shape%s"%suffix)

  plot(graphs, hmaxes, cats, mlow, mhigh, opt.nBins, blind, outpath)
  f.Close()


if __name__ == "__main__":
  main()
