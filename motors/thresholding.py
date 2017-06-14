"""
These functions will be used to produce a family of curves, showing 
flux above certain thresholds, changes wiht concentration.

"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import aesthetics as aesthetics

def return_concentration_slice(df, concentration):
    tmp = df[np.round(df['Concentration'], 1) ==  np.round(concentration, 1)]
    return tmp

def find_above_threshold(df, threshold):
    concentrations = []
    number_above_threshold = []
    for concentration in np.unique(df['Concentration'].values):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10**concentration)
        number_above_threshold.append(sum(tmp['Directional flux'].abs() > threshold))   
    return concentrations, number_above_threshold

def find_driven_above_threshold(df, threshold):
    concentrations = []
    number_above_threshold = []
    for concentration in np.unique(df['Concentration'].values):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10**concentration)
        number_above_threshold.append(sum(tmp['Driven flux'].abs() > threshold))   
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


def plot_families(df, thresholds, color=None, xmin=10**-7, xmax=10**0, ymin=-10, ymax=200):
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax = plt.subplot(gs[0, 0])
    cmap = sns.cubehelix_palette(len(thresholds))

    for threshold in thresholds:
        x, y = find_above_threshold(df, threshold)
        ax.plot(x, y, c=cmap[np.where(thresholds==threshold)[0]], label='{}'.format(threshold))
    
    ax.set_xlabel('Substrate concentration (M)')
    ax.set_ylabel('Number of angles over threshold')
    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, title='Flux (cycle s$^{{-1}}$)')
    aesthetics.paper_plot(fig)
    

def save_families(df, thresholds, name, catalytic_rate):

    tmp = pd.DataFrame()
    for threshold in thresholds:
        x, y = find_above_threshold(df, threshold)
        for data_point in range(len(x)):
            tmp = tmp.append(pd.DataFrame({'Flux threshold': threshold,
                                           'Number of angles': y[data_point],
                                           'Concentration (M)': x[data_point],
                                           'Catalytic rate (per second)': catalytic_rate,
                                          }, index=[0]), ignore_index=True)
    tmp.to_csv(name)

def plot_histograms(df, concentration, color):

    tmp = return_concentration_slice(df, concentration)
    flux = tmp['Directional flux'].abs().values
    hist, bin_edges = np.histogram(flux, bins=20)
    mids = bin_edges[1:] - np.diff(bin_edges)/2
    print('Edge, Edge, Count')
    for i in range(len(hist)):
        print(bin_edges[i], bin_edges[i+1], hist[i])
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax = plt.subplot(gs[0, 0])
    rects = ax.bar(mids, hist, width=10, color=color)
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            i = rects.index(rect)
            plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '{}'.format(int(height)),
                    ha='center', va='bottom')
    autolabel(rects)
    ax.set_ylabel('Count')
    ax.set_xlabel('Directional flux (cycle s$^{{-1}}$)')
    aesthetics.paper_plot(fig)
    