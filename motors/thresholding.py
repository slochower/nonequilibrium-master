"""
These functions will be used to produce a family of curves, showing 
flux above certain thresholds, changes wiht concentration.

"""
import numpy as np
import pandas as pd


def find_above_threshold(df, quantity, threshold):
    concentrations = []
    number_above_threshold = []
    for concentration in tqdm(np.unique(df['Concentration'].values)):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10 ** concentration)
        number_above_threshold.append(sum(tmp[str(quantity)].abs() > threshold))
    return concentrations, number_above_threshold


def find_stall_above_threshold(df, threshold):
    concentrations = []
    number_above_threshold = []
    for concentration in np.unique(df['Concentration'].values):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10**concentration)
        # The factor of 2 here is because 'Max load' is actually 'Load @ max power',
        # which is about half of the true stall load.
        number_above_threshold.append(sum(2* tmp['Max load'].abs() > threshold))   
    return concentrations, number_above_threshold


def find_power_above_threshold(df, threshold):
    concentrations = []
    number_above_threshold = []
    for concentration in np.unique(df['Concentration'].values):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10**concentration)
        number_above_threshold.append(sum(tmp['Max power'].abs() > threshold))   
    return concentrations, number_above_threshold


    
