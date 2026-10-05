import ROOT
f = ROOT.TFile.Open("Datacard_tth_th_cp_Analysis_cpTopHiggs.root")
w = f.Get("w")
it = w.allVars().createIterator()
var = it.Next()
while var:
    print(var.GetName(), var.getVal(), var.getError(), var.getMin(), var.getMax())
    var = it.Next()