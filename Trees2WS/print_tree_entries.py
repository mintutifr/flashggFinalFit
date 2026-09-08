#!/usr/bin/env python3
# Script to print the number of entries in every TTree found inside a ROOT file

import argparse
import ROOT

def get_options():
  parser = argparse.ArgumentParser(description="Print entries of all TTrees inside a ROOT file")
  parser.add_argument('--input', dest='input', required=True, help='Input ROOT file')
  parser.add_argument('--tree', dest='tree', default=None, help='Only print entries for this specific tree (name or full path, e.g. DiphotonTree/Data_13TeV_ttH_had0_CP_odd)')
  return parser.parse_args()

def find_trees(directory, path=""):
  trees = []
  for key in directory.GetListOfKeys():
    className = key.GetClassName()
    name = key.GetName()
    fullPath = "%s/%s" % (path, name) if path else name
    if className.startswith("TTree"):
      obj = directory.Get(name)
      trees.append((fullPath, obj.GetEntries()))
    elif className in ("TDirectoryFile", "TDirectory"):
      subdir = directory.Get(name)
      trees.extend(find_trees(subdir, fullPath))
  return trees

def main():
  opt = get_options()
  f = ROOT.TFile.Open(opt.input)
  if not f or f.IsZombie():
    print(" --> [ERROR] Could not open file: %s" % opt.input)
    return

  trees = find_trees(f)

  if opt.tree is not None:
    matches = [(name, entries) for name, entries in trees if name == opt.tree or name.split("/")[-1] == opt.tree]
    if not matches:
      print(" --> [ERROR] Tree '%s' not found in %s" % (opt.tree, opt.input))
      print(" --> Available trees:")
      for name, _ in trees: print("    * %s" % name)
      return
    for name, entries in matches:
      print("%s : %d entries" % (name, entries))
    return

  if not trees:
    print(" --> No TTrees found in %s" % opt.input)
    return

  nameWidth = max(len(name) for name, _ in trees)
  print(" --> Trees in %s" % opt.input)
  for name, entries in trees:
    print("    * %-*s : %d entries" % (nameWidth, name, entries))
  print(" --> Total: %d trees, %d entries" % (len(trees), sum(e for _, e in trees)))

if __name__ == "__main__":
  main()
