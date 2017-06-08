#!/usr/bin/env python
"""
These functions slice flux, power, and load from pickle files that contain the results
of scanning across concentration.
"""

from simulation import *


def summarize_fluxes(name, concentration, data_source='adk_md_data', catalytic_rate=None):
    """
    Report fluxes for a file at a given concentration.
    :param name:
    :param concentration:
    :param data_source:
    :param catalytic_rate:
    :return:
    """
    this = Simulation(data_source=data_source)
    this.cSubstrate = concentration
    if catalytic_rate:
        this.catalytic_rate = catalytic_rate
    this.name = name
    this.simulate()
    directional_flux = np.mean(this.flux_u + this.flux_b)
    intersurface_flux = max(abs(this.flux_ub))
    # Make all flux on each surface positive
    unbound_flux = abs(this.flux_u)
    bound_flux = abs(this.flux_b)
    # Now find the maximum on either surface
    max_unbound = max(unbound_flux)
    max_bound = max(bound_flux)
    driven_flux = max([max_unbound, max_bound])
    return directional_flux, intersurface_flux, driven_flux


def summarize_power_and_load(name, concentration, data_source='adk_md_data', negative=False,
                             debug=False, catalytic_rate=None):
    """
    Return power and load for a file at a given concentration.
    :param name:
    :param concentration:
    :param data_source:
    :param negative:
    :param debug:
    :param catalytic_rate:
    :return:
    """
    this = Simulation(data_source=data_source)
    this.cSubstrate = concentration
    if catalytic_rate:
        this.catalytic_rate = catalytic_rate
    this.name = name
    # The difference now, is that we're going to need to simulate with
    # an applied load.
    this.load = True
    # Initialize the applied load to be something small, and we'll increase
    # from there on out.
    slope = 0.000
    increment = 0.00001
    loads = []
    power_given_load = []
    flux_given_load = []
    if debug:
        plt.figure()
        plt.xlabel('Load')
        plt.ylabel('Power')
    while True:
        if negative:
            this.load_slope = -slope
        else:
            this.load_slope = slope
        this.simulate()
        # Bookkeeping
        flux = np.mean(this.flux_u + this.flux_b)
        power = this.load_slope * np.mean(this.flux_u + this.flux_b)
        loads.append(this.load_slope)
        flux_given_load.append(flux)
        power_given_load.append(power)
        if debug:
            plt.scatter(this.load_slope, power)
            print('{0:1.6f}\t{1:1.6f}'.format(this.load_slope, power))
        # Now, we need to check the power trend to see if we should break
        # out of the loop.
        max_power = max(power_given_load)
        max_power_index = power_given_load.index(max_power)
        # Is the maximum power the last element?
        if max_power > power_given_load[0] and max_power > power_given_load[-1]:
            # print('Looks good. Maximum power = {} with load = {}'.format(
            #    max_power, loads[max_power_index]))
            # But let's check and make sure the power doesn't continue to increase,
            # before we break
            slope += increment
            if negative:
                this.load_slope = -slope
            else:
                this.load_slope = slope
            this.simulate()
            power = this.load_slope * np.mean(this.flux_u + this.flux_b)
            if max_power > power:
                # break
                return max_power, loads[max_power_index]
        if max_power == 0 and len(power_given_load) > 100:
            # Sometimes this happens...
            # We should probably make a note of this too. Ugh.
            # This can happen if the maximum load that can be supported is even
            # smaller than the increment size.
            return 0.0, 0.0
        if len(power_given_load) % 100 == 0:
            increment *= 10
        if len(power_given_load) > 1000:
            print('I give up.')
        if slope > 10:
            print('This doesn\'t make sense.')
            break
        slope += increment
    del this
