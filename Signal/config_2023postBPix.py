# Config file: options for signal fitting

_year = '2023postBPix'

signalScriptCfg = {
  
  # Setup
  'inputWSDir':'/eos/user/m/mikumar/Final_fits/outputForFinalFits_7Sep2026/workspaces/%s/'%_year,
  'procs': 'auto', #'auto', # if auto: inferred automatically from filenames
  'cats': 'tHq_had0_CP_odd,tHq_had0_CP_even,ttH_had0_CP_even,ttH_had0_CP_odd,tHq_had0_CP_mix', #'auto', #'ttH_lep0_CP_even', #'auto', # if auto: inferred automatically from (0) workspace
  'ext':'tth_th_cp_Analysis', #_%s'%_year,
  'analysis':'tth_th_cp_Analysis', # To specify which replacement dataset mapping (defined in ./python/replacementMap.py)
  'year':'%s'%_year, # Use 'combined' if merging all years: not recommended
  'massPoints':'125',

  #Photon shape systematics  
  'scales':'', #'Scale', # separate nuisance per year
  'scalesCorr':'', # correlated across years
  'scalesGlobal':'', # affect all processes equally, correlated across years
  'smears':'', #'Smearing', # separate nuisance per year

  # Job submission options
  'batch':'local', # ['condor','SGE','IC','local']
  'queue':'espresso',

}
