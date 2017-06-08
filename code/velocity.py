"""
These functions will be used to plot the enzyme velocity and
the enzyme flux on a graph with two y axes. Each graph will have three
curves: directional flux, reciprocating lfux, and motor velocity.
We will probably need to calculate the velocity directly, because I don't
think there is a way to extract it from the existing data in the pickle.
In which case, I might just compute all three curves together.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import aesthetics as aesthetics
from simulation import *

def return_concentration_slice(df, concentration):
    tmp = df[np.round(df['Concentration'], 1) ==  np.round(concentration, 1)]
    return tmp

def return_fluxes_and_velocity(protein, name, concentrations):
    directional_flux, reciprocating_flux, velocity = [], [], []
    for concentration in concentrations:
        print('Concentration = {}'.format(concentration))
        this = simulation(data_source=protein)
        this.name = name
        this.cSubstrate = concentration
        this.simulate()
        directional_flux.append(np.mean(this.flux_u + this.flux_b))
        reciprocating_flux.append(np.max(np.hstack((abs(this.flux_u), abs(this.flux_b)))))
        velocity.append(np.sum(this.ss[this.bins:2*this.bins]) * this.catalytic_rate)

    return directional_flux, reciprocating_flux, velocity


def plot_fluxes_and_velocity(concentrations, directional_flux, reciprocating_flux, velocity,
                             ymin1=None, ymax1=None,):

    cmap = sns.color_palette("Paired", 10)
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])

    ax1.plot(concentrations, velocity, c=cmap[1])
    ax1.set_xscale('log')
    ax1.set_ylabel(r'Catalytic rate (turnover s$^{{-1}}$)', color=cmap[1])

    ax1.set_ylim([ymin1, ymax1])

    ax2 = ax1.twinx()
    ax2.plot(concentrations, [abs(i) for i in directional_flux], c=cmap[3])
    ax2.plot(concentrations, [abs(i) for i in reciprocating_flux], c=cmap[3], ls='--')
    ax2.set_ylabel('Directional and reciprocating flux\n(cycle s$^{{-1}}$)', color=cmap[3])
    ax2.set_ylim([ymin1, ymax1])

    for tl in ax1.get_yticklabels():
        tl.set_color(cmap[1])
    for tl in ax2.get_yticklabels():
        tl.set_color(cmap[3])

    ax1.set_xlabel('Substrate concentration (M)')
    for ax in fig.axes:
        ax.tick_params(which='major', direction='out', length=10, pad=10)
        ax.tick_params(which='minor', direction='out', length=5)
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.xaxis.set_ticks_position('bottom')
        ax.spines["top"].set_visible(False)
        ax.xaxis.labelpad = 15
        ax.yaxis.labelpad = 15
    fig.patch.set_facecolor('white')