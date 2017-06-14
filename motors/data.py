import glob as glob

pka_dir = '../../md-data/pka-md-data/'
pka_unbound_files = sorted(glob.glob(pka_dir + 'apo/' + '*'))

adk_dir = '../../md-data/adk-md-data/'
adk_unbound_files = sorted(glob.glob(adk_dir + 'apo/' + '*'))
