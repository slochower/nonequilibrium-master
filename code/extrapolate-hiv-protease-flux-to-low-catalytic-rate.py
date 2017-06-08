"""
These functions will report how the flux changes with catalytic rate
constant for HIVP, to extrapolate the behavior of the angles at low 
catalytic rate (0.3 per second) without the noise of actually simulating
at that low rate.
"""

import numpy as np
from scipy import stats
import glob as glob
import os as os
import re as re
import pandas as pd

def return_concentration_slice(df, concentration):
    tmp = df[np.round(df['Concentration'], 1) ==  np.round(concentration, 1)]
    return tmp


hiv_dir = '../../md-data/hiv-protease/'
hiv_unbound_files = sorted(glob.glob(hiv_dir + '1hhp_apo/' + '*'))
names = []
for file in range(len(hiv_unbound_files)):
    name = os.path.splitext(os.path.basename(hiv_unbound_files[file]))[0]
    name = re.search('^[^_]*', name).group(0)        
    if re.search('omega*', name):
        continue
    if re.search('chi3ASN*', name):
        continue
    if re.search('chi5LYS*', name):
        continue
        continue
    names.append(name)
    
concentrations = [300, 200, 100, 10]
hiv_300 = pd.read_pickle('hiv-high-catalytic-rate-300.pickle')
hiv_200 = pd.read_pickle('hiv-high-catalytic-rate-200.pickle')
hiv_100 = pd.read_pickle('hiv-high-catalytic-rate-100.pickle')
hiv_10 = pd.read_pickle('hiv-high-catalytic-rate-10.pickle')
dfs = [hiv_300, hiv_200, hiv_100, hiv_10]

hiv_pointthree = pd.DataFrame()

for concentration in np.arange(-6, 0, 0.1):
    print('Concentration = {}'.format(concentration))
    for name in names:
        fluxes = []
        for df in dfs:
            tmp = return_concentration_slice(df, concentration)
            fluxes.append(tmp[tmp['File'] == name]['Directional flux'].values[0])
        # plt.scatter(concentrations, fluxes)
        slope, intercept, r_value, p_value, std_err = stats.linregress(concentrations, fluxes)
        # print('{}\t{}'.format(name, slope))
        def y(slope, intercept, x):
            return slope * x + intercept 
        # print('Flux @ 0.3\t{}'.format(y(slope, intercept, 0.3)))
        # For chi2ASP124, a well behaved angle, the actual flux at [S] = 0.1 M and 
        # k_{catalysis} = 0.3 per second, is -0.168, so not that far off from the
        # extrapolated value of -0.176. But a little more wiggle room than I would
        # have expected because the line does seem quite tight.
        hiv_pointthree = hiv_pointthree.append(pd.DataFrame({'File': name,
                                                            'Flux': y(slope, intercept, 0.3),
                                                            'Concentration': concentration
        }, index=[0]), ignore_index=True)
hiv_pointthree.to_pickle('hiv_pointthree.pickle')
