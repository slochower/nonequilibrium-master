#!/usr/bin/env python
"""
This has a single class: `Simulation`
This class contains the code to calculate probability flux given two equilibrium
population distributions.
"""

import math as math
import numpy as np
import seaborn as sns
import os as os
from scipy.ndimage.filters import gaussian_filter


class Simulation(object):
    """
    This class contains the code to calculate probability flux given two equilibrium
    population distributions.
    """
    # This is a complicated class, we want more than seven attributes:
    # pylint: disable=too-many-instance-attributes
    # To use physically meaningful attribute names (i.e., kT):
    # pylint: disable=C0103

    def __init__(self, data_source):
        """
        These values are assigned to a new object, unless overridden later.
        """
        # Model parameters
        self.kT = 0.6  # RT = 0.6 kcal per mol
        # The butane-derived D value is 3 * 10 ** 15, but we've now shown that
        # a lower value can be safely used without changing the results much.
        self.D = 3 * 10 ** 12  # degree**2 per second
        # Implementation parameters
        self.dir = None
        self.data_source = data_source
        if self.data_source == 'pka_md_data' or self.data_source == 'pka_reversed':
            self.C_intersurface = 0.24 * 10 ** 6  # per mole per second
            self.offset_factor = 6.0  # kcal per mol
            self.catalytic_rate = 140.0  # per second
            self.cSubstrate = 2 * 10 ** -3  # ATP concentration (M)
        elif self.data_source == 'adk_md_data':
            self.C_intersurface = 10.0 ** 6  # per mole per second
            self.offset_factor = 5.7  # kcal per mol
            self.catalytic_rate = 312.0  # per second
            # Let's say ATP concentration = 9 * 10**-3 M and AMP concentration = 2.8 * 10**-4 M
            # Absolute metabolite concentrations and implied enzyme active site occupancy in
            # Escherichia coli (2009), Nat Chem Biol
            # ATP.AMP concentration (M) as a single concentration
            self.cSubstrate = 2.5 * 10 ** -6
        elif self.data_source == 'hiv_md_data':
            self.C_intersurface = 10.0 ** 6  # per mole per second
            self.offset_factor = 4.5  # kcal per mol
            self.catalytic_rate = 0.3  # per second
            self.cSubstrate = 2 * 10 ** -3  # Gag concentration (M)
        elif self.data_source == 'manual':
            # print('Using manual parameters, specify C, offset, and catalytic rate.')
            pass
        else:
            print('No data source; no values for C, offset, and catalytic rate')

        # The name needs to be provided at runtime, unless the data source is
        # manual.
        self.name = None
        # The initial populations are empty, until parsed from the files.
        self.unbound_population = []
        self.bound_population = []
        # The PDFs are derived from the populations.
        self.PDF_unbound = None
        self.PDF_bound = None
        # The rates will be calculated from the energy surfaces.
        self.forward_rates = None
        self.backward_rates = None
        # The transition matrix is composed from the rates.
        self.tm = None
        # The time step `dt` is determined so all elements in the transition
        # matrix are in [0, 1).
        self.dt = None
        # The eigenvalues and steady state population are calculated from the
        # transition matrix.
        self.eigenvalues = None
        self.ss = None
        # The surface fluxes are calculated using the rates and the
        # populations.
        self.flux_u = None
        self.flux_b = None
        self.flux_ub = None

        # By default, we run without any applied load on the motor.
        self.load = False
        if self.load:
            self.load_slope = self.bins  # kcal per mol per (2 * pi) radians
        else:
            self.load_slope = 0
        # By default, we run without any artifical barriers imposed on the
        # motor.
        self.barrier = False
        if self.barrier:
            self.barrier_bin = 0

    def data_to_energy(self, histogram):
        """
        This function takes in population histograms from Chris' PKA data and
        (a) smooths them with a Gaussian kernel with width 1;
        (b) eliminates zeros by setting any zero value to the minimum of the data;
        (c) turns the population histograms to energy surfaces.
        """

        histogram_smooth = gaussian_filter(histogram, 1)
        histogram_copy = np.copy(histogram_smooth)
        for i in range(len(histogram)):
            if histogram_smooth[i] != 0:
                histogram_copy[i] = histogram_smooth[i]
            else:
                histogram_copy[i] = min(
                    histogram_smooth[np.nonzero(histogram_smooth)])
        histogram_smooth = histogram_copy
        assert not np.any(histogram_smooth == 0)
        histogram_smooth = histogram_smooth / np.sum(histogram_smooth)
        energy = -self.kT * np.log(histogram_smooth)
        return energy

    def calculate_boltzmann(self):
        """
        This function calculates the normalized steady state probability density, given populations.
        """
        boltzmann_unbound = np.exp(-1 * np.array(self.unbound) / self.kT)
        boltzmann_bound = np.exp(-1 * np.array(self.bound) / self.kT)
        self.PDF_unbound = boltzmann_unbound / np.sum(boltzmann_unbound)
        self.PDF_bound = boltzmann_bound / np.sum(boltzmann_bound)

    def calculate_intrasurface_rates(self, energy_surface):
        """
        This function calculates intrasurface rates using the energy difference between
        adjacent bins.
        """

        forward_rates = self.C_intrasurface * \
            np.exp(-1 * np.diff(energy_surface) / float(2 * self.kT))
        backward_rates = self.C_intrasurface * \
            np.exp(+1 * np.diff(energy_surface) / float(2 * self.kT))
        rate_matrix = np.zeros((self.bins, self.bins))
        for i in range(self.bins - 1):
            rate_matrix[i][i + 1] = forward_rates[i]
            rate_matrix[i + 1][i] = backward_rates[i]
        rate_matrix[0][self.bins - 1] = self.C_intrasurface * np.exp(
            -(energy_surface[self.bins - 1] - energy_surface[0]) / float(2 * self.kT))
        rate_matrix[self.bins - 1][0] = self.C_intrasurface * np.exp(
            +(energy_surface[self.bins - 1] - energy_surface[0]) / float(2 * self.kT))
        return rate_matrix

    def calculate_intrasurface_rates_with_load(self, energy_surface):
        """
        This function calculates intrasurface rates using the energy difference between
        adjacent bins,
        this function is distinct from `calculate_intrasurface_rates` because the load function
        has different boundary conditions than the energy function. The energy function has perfect
        periodic
        boundary conditions, but the load must continue to decrease or increase across the
        boundaries.
        """
        surface_with_load = np.hstack(
            ([energy_surface[i] + self.load_function(i) for i in range(self.bins)]))
        # This should handle the interior elements just fine.
        self.forward_rates = self.C_intrasurface * \
            np.exp(-1 * np.diff(surface_with_load) / float(2 * self.kT))
        self.backward_rates = self.C_intrasurface * \
            np.exp(+1 * np.diff(surface_with_load) / float(2 * self.kT))
        rate_matrix = np.zeros((self.bins, self.bins))

        for i in range(self.bins - 1):
            rate_matrix[i][i + 1] = self.forward_rates[i]
            rate_matrix[i + 1][i] = self.backward_rates[i]

        # But now the PBCs are a little tricky...
        rate_matrix[0][self.bins - 1] = self.C_intrasurface * np.exp(
            -(energy_surface[self.bins - 1] + self.load_function(-1) -
              (energy_surface[0] + self.load_function(0))) / float(2 * self.kT))

        rate_matrix[self.bins - 1][0] = self.C_intrasurface * np.exp(
            +(energy_surface[self.bins - 1] + self.load_function(self.bins - 1) -
              (energy_surface[0] + self.load_function(self.bins))) / float(2 * self.kT))

        return rate_matrix

    def calculate_intersurface_rates(self, unbound_surface, bound_surface):
        """
        This function calculates the intersurface rates in two ways.
        For bound to unbound, the rates are calculated according to the energy difference and
        the catalytic rate.
        For unbound to bound, the rates depend on the prefactor and the concentration of substrate.
        """

        bu_rm = np.empty((self.bins))
        ub_rm = np.empty((self.bins))
        for i in range(self.bins):
            bu_rm[i] = (self.C_intersurface *
                        np.exp(-1 * (unbound_surface[i] - bound_surface[i]) / float(self.kT)) +
                        self.catalytic_rate)
            ub_rm[i] = self.C_intersurface * self.cSubstrate
        return ub_rm, bu_rm

    def compose_tm(self, u_rm, b_rm, ub_rm, bu_rm):
        """
        We take the four rate matrices (two single surface and two intersurface) and inject them
        into the transition matrix.
        """

        tm = np.zeros((2 * self.bins, 2 * self.bins))
        tm[0:self.bins, 0:self.bins] = u_rm
        tm[self.bins:2 * self.bins, self.bins:2 * self.bins] = b_rm
        for i in range(self.bins):
            tm[i, i + self.bins] = ub_rm[i]
            tm[i + self.bins, i] = bu_rm[i]
        self.tm = self.scale_tm(tm)
        return

    def scale_tm(self, tm):
        """
        The transition matrix is scaled by `dt` so all rows sum to 1 and
        all elements are less than 1.
        This should not use `self` subobjects, except for `dt`
        because we are mutating the variables.
        """

        row_sums = tm.sum(axis=1, keepdims=True)
        maximum_row_sum = int(math.log10(max(row_sums)))
        self.dt = 10 ** -(maximum_row_sum + 1)
        tm_scaled = self.dt * tm
        row_sums = tm_scaled.sum(axis=1, keepdims=True)
        if np.any(row_sums > 1):
            print('Row sums unexpectedly greater than 1.')
        for i in range(2 * self.bins):
            tm_scaled[i][i] = 1.0 - row_sums[i]
        return tm_scaled

    def calculate_eigenvector(self):
        """
        The eigenvectors and eigenvalues of the transition matrix are computed and the steady-state
        population is assigned to the eigenvector with an eigenvalue of 1.
        """

        self.eigenvalues, eigenvectors = np.linalg.eig(np.transpose(self.tm))
        ss = abs(eigenvectors[:, self.eigenvalues.argmax()].astype(float))
        self.ss = ss / np.sum(ss)
        return

    def calculate_flux(self, ss, tm):
        """
        This function calculates the intrasurface flux using the steady-state distribution and the
        transition matrix.
        The steady-state distribution is a parameter so this function can be run with either the
        eigenvector-derived steady-state distribution or the interated steady-state distribution.
        """

        flux_u = np.empty((self.bins))
        flux_b = np.empty((self.bins))
        flux_ub = np.empty((self.bins))
        for i in range(self.bins):
            if i == 0:
                flux_u[i] = -1 * (- ss[i] * tm[i][i + 1] /
                                  self.dt + ss[i + 1] * tm[i + 1][i] / self.dt)
            if i == self.bins - 1:
                flux_u[i] = -1 * (- ss[i] * tm[i][0] /
                                  self.dt + ss[0] * tm[0][i] / self.dt)
            else:
                flux_u[i] = -1 * (- ss[i] * tm[i][i + 1] /
                                  self.dt + ss[i + 1] * tm[i + 1][i] / self.dt)
        for i in range(self.bins, 2 * self.bins):
            if i == self.bins:
                flux_b[i - self.bins] = -1 * \
                    (- ss[i] * tm[i][i + 1] / self.dt +
                     ss[i + 1] * tm[i + 1][i] / self.dt)
            if i == 2 * self.bins - 1:
                flux_b[i - self.bins] = -1 * (
                    - ss[i] * tm[i][self.bins] / self.dt + ss[self.bins] * tm[self.bins][i] / self.dt)
            else:
                flux_b[i - self.bins] = -1 * \
                    (- ss[i] * tm[i][i + 1] / self.dt +
                     ss[i + 1] * tm[i + 1][i] / self.dt)
        for i in range(self.bins):
            flux_ub[i] = -1 * (
                - ss[i] * tm[i][i + self.bins] / self.dt + ss[i + self.bins] * tm[i + self.bins][i] / self.dt)

        self.flux_u = flux_u
        self.flux_b = flux_b
        self.flux_ub = flux_ub
        return

    def simulate(self, user_energies=False, catalysis=True):
        """
        Now this function takes in a file(name) and determins the energy surfaces automatically,
        so I don't forget to do it in an interactive session.
        This function runs the `simulation` which involves:
        (a) setting the unbound intrasurface rates,
        (b) setting the bound intrasurface rates,
        (c) setting the intersurface rates,
        (d) composing the transition matrix,
        (e) calculating the eigenvectors of the transition matrix,
        (f) calculating the intrasurface flux,
        and optionally (g) running an interative method to determine the steady-state distribution.
        """
        if self.data_source == 'pka_md_data':
            self.dir = os.path.join(os.path.dirname(
                __file__), '../md-data/pka-md-data')
            try:
                self.unbound_population = np.genfromtxt(self.dir + '/apo/' + self.name +
                                                        '_chi_pop_hist_targ.txt',
                                                        delimiter=',',
                                                        skip_header=1)
                self.bound_population = np.genfromtxt(self.dir + '/atpmg/' + self.name +
                                                      '_chi_pop_hist_ref.txt',
                                                      delimiter=',',
                                                      skip_header=1)
            except IOError:
                print('Cannot read {} from {}.'.format(self.name, self.dir))
            cmap = sns.color_palette("Paired", 10)
            self.unbound_clr = cmap[6]
            self.bound_clr = cmap[7]

        elif self.data_source == 'pka_reversed':
            self.dir = os.path.join(os.path.dirname(
                __file__), '../md-data/pka-md-reversed-and-averaged')
            try:
                self.unbound_population = np.genfromtxt(self.dir + '/apo/' + self.name +
                                                        '_chi_pop_hist_targ.txt',
                                                        delimiter=',',
                                                        skip_header=1)
                self.bound_population = np.genfromtxt(self.dir + '/atpmg/' + self.name +
                                                      '_chi_pop_hist_ref.txt',
                                                      delimiter=',',
                                                      skip_header=1)

            except IOError:
                print('Cannot read {} from {}.'.format(self.name, self.dir))

            cmap = sns.color_palette("Paired", 10)
            self.unbound_clr = cmap[6]
            self.bound_clr = cmap[7]

        elif self.data_source == 'adk_md_data':
            self.dir = os.path.join(os.path.dirname(
                __file__), '../md-data/adenylate-kinase')
            try:
                self.unbound_population = np.genfromtxt(self.dir + '/AdKDihedHist_apo-4ake/' +
                                                        self.name + '.dat',
                                                        delimiter=' ',
                                                        skip_header=1,
                                                        usecols=1)
                self.bound_population = np.genfromtxt(self.dir + '/AdKDihedHist_ap5-3hpq/' +
                                                      self.name + '.dat',
                                                      delimiter=' ',
                                                      skip_header=1,
                                                      usecols=1)

            except IOError:
                print('Cannot read {} from {}.'.format(self.name, self.dir))

            cmap = sns.color_palette("Paired", 10)
            self.unbound_clr = cmap[3]
            self.bound_clr = cmap[1]

        elif self.data_source == 'hiv_md_data':
            self.dir = os.path.join(os.path.dirname(
                __file__), '../md-data/hiv-protease')
            try:
                self.unbound_population = np.genfromtxt(self.dir + '/1hhp_apo/' +
                                                        self.name + '.dat',
                                                        delimiter=' ',
                                                        skip_header=1,
                                                        usecols=1)
                self.bound_population = np.genfromtxt(self.dir + '/1kjf_p1p6/' +
                                                      self.name + '.dat',
                                                      delimiter=' ',
                                                      skip_header=1,
                                                      usecols=1)

            except IOError:
                print('Cannot read {} from {}.'.format(self.name, self.dir))

            cmap = sns.color_palette("Paired", 10)
            self.unbound_clr = cmap[2]
            self.bound_clr = cmap[3]

        elif self.data_source == 'manual':
            # Populations are supplied manually.
            cmap = sns.color_palette("Paired", 10)
            self.unbound_clr = cmap[8]
            self.bound_clr = cmap[9]
        else:
            print('No populations.')
        if user_energies:
            pass
        else:
            self.unbound = self.data_to_energy(self.unbound_population)
            self.bound = self.data_to_energy(
                self.bound_population) - self.offset_factor

        self.bins = len(self.unbound)
        self.tm = np.zeros((self.bins, self.bins))
        self.C_intrasurface = self.D / \
            (360. / self.bins) ** 2  # per degree per second

        if not self.load:
            u_rm = self.calculate_intrasurface_rates(self.unbound)
            b_rm = self.calculate_intrasurface_rates(self.bound)
        if self.load:
            u_rm = self.calculate_intrasurface_rates_with_load(self.unbound)
            b_rm = self.calculate_intrasurface_rates_with_load(self.bound)

        if self.barrier:
            u_rm[self.barrier_bin][self.barrier_bin + 1] = 0
            u_rm[self.barrier_bin + 1][self.barrier_bin] = 0
            b_rm[self.barrier_bin][self.barrier_bin + 1] = 0
            b_rm[self.barrier_bin + 1][self.barrier_bin] = 0

        ub_rm, bu_rm = self.calculate_intersurface_rates(
            self.unbound, self.bound)
        self.compose_tm(u_rm, b_rm, ub_rm, bu_rm)
        self.calculate_eigenvector()
        self.calculate_boltzmann()
        self.calculate_flux(self.ss, self.tm)

        return

    def load_function(self, x):
        return x * self.load_slope / self.bins
