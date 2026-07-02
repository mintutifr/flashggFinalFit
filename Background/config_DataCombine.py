# Config file: options for signal fitting

backgroundScriptCfg = {
  # Setup
  'inputWS':'/eos/user/m/mikumar/Final_fits/outputForFinalFits_25June2026/root/Data/ws/allData.root', # location of 'allData.root' file
  'cats': 'ttH_had0_CP_even,ttH_had0_CP_odd', #'auto', #'ttH_had0_CP_even',#'auto', # auto: automatically inferred from input ws
  'catOffset':0, # add offset to category numbers (useful for categories from different allData.root files)  
  'ext':'tth_th_cp_Analysis', # extension to add to output directory
  'year':'combined', # Use combined when merging all years in category (for plots)

  # Job submission options
  'batch':'local', #'condor', # [condor,SGE,IC,local]
  'queue':'espresso' # for condor e.g. microcentury
  
}
