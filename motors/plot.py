import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.gridspec import GridSpec
from tqdm import tqdm
from motors.aesthetics import prepare_plot
from motors.aesthetics import paper_plot
from motors.simulation import Simulation


def plot_input(this, save=False, filename=None):
    """
    This function plots the unbound and bound histograms as a function of dihedral angle. The input histograms
    are taken to be normalized populations derived from MD simulations.
    :param this: an object of class Simulation that contains `this.unthis.bound_population` and `this.bound_population` attributes,
    at minimum
    :param save: whether to save the plot to a file
    :param filename: name of file
    :return:
    """

    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax1.plot(range(this.bins), this.unbound_population, c=this.unbound_clr)
    ax1.plot(range(this.bins), this.bound_population,
             c=this.bound_clr, ls='--')
    ax1.set_xticks([0, this.bins / 4, this.bins /
                    2, 3 * this.bins / 4, this.bins])
    ax1.set_xticklabels(
        [r'$-\pi$', r'$-\frac{1}{2}\pi{}$', r'$0$', r'$\frac{1}{2}\pi$', r'$\pi$'])
    ax1.set_xlabel(r'$\theta$ (rad)')
    ax1.set_ylabel(r'$p$ (input population)')
    paper_plot(fig, scientific=False)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')


def plot_energy(this, save=False, filename=None):
    """
    This function plots the unbound and bound energies (i.e., chemical potentials)
    associated with a Simulation object.
    """

    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax1.plot(range(this.bins), this.unbound, c=this.unbound_clr)
    ax1.plot(range(this.bins), this.bound, c=this.bound_clr, ls='--')
    ax1.set_xticks([0, this.bins / 4, this.bins /
                    2, 3 * this.bins / 4, this.bins])
    ax1.set_xticklabels(
        [r'$-\pi$', r'$-\frac{1}{2}\pi{}$', r'$0$', r'$\frac{1}{2}\pi$', r'$\pi$'])
    ax1.set_xlabel(r'$\theta$ (rad)')
    ax1.set_ylabel(r'$\mu$ (kcal mol$^{-1}$)')
    paper_plot(fig, scientific=False)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')
        # return fig


def plot_ss(this, save=False, filename=None):
    """
    This function plots the nonequilibrium steady-state distribution associated
    with a Simulation object.
    By default, this will plot the eigenvector-derived steady-state distribution.
    """

    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax1.plot(range(this.bins), this.ss[0:this.bins], c=this.unbound_clr)
    ax1.plot(range(this.bins),
             this.ss[this.bins:2 * this.bins], c=this.bound_clr, ls='--')
    ax1.set_xticks([0, this.bins / 4, this.bins /
                    2, 3 * this.bins / 4, this.bins])
    ax1.set_xticklabels(
        [r'$-\pi$', r'$-\frac{1}{2}\pi{}$', r'$0$', r'$\frac{1}{2}\pi$', r'$\pi$'])
    ax1.set_xlabel(r'$\theta$ (rad)')
    ax1.set_ylabel(r'$p$ (probability)')
    paper_plot(fig, scientific=False)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')
        # return fig


def print_parameter(label, value, unit):
    """
    This function pretty prints some class variables for the flux plots.
    :param label:
    :param value:
    :param unit:
    :return:
    """
    print('{:<25} {:<+10.2e} {:<10}'.format(label, value, unit))


def plot_flux(this, save=False, filename=None):
    """
    This function plots the intrasurface flux separately and as a sum. The intrasurface flux
    is the directional flux. This also prints the simulation parameters.
    """

    print_parameter('C', this.C_intersurface, 'second**-1')
    print_parameter('D', this.D, 'degrees**2 second**-1')
    print_parameter('k_{cat}', this.catalytic_rate, 'second**-1')
    print_parameter('[S]', this.cSubstrate, 'M')
    print_parameter('dt', this.dt, 'second')
    print('-' * 25)
    print_parameter('Intrasurface flux', np.mean(
        this.flux_u + this.flux_b), 'cycle second**-1')
    print_parameter('Peak', np.max(
        np.hstack((this.flux_u, this.flux_b))), 'cycle second**-1')
    if this.load:
        print('-' * 25)
        applied_load = this.load_slope
        power = applied_load * np.mean(this.flux_u + this.flux_b)
        print_parameter('Applied load', applied_load, 'kcal mol**-1 cycle**-1')
        print_parameter('Power generated', power, 'kcal mol**-1 second**-1')

    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax1.plot(range(this.bins), this.flux_u, c=this.unbound_clr)
    ax1.plot(range(this.bins), this.flux_b, c=this.bound_clr, ls='--')
    ax1.plot(range(this.bins), this.flux_u + this.flux_b, 'o', c='k',
             lw=2, alpha=0.5, zorder=-1, label='Net flux')
    # ax1.scatter(range(this.bins), flux_u + flux_b, c='k', marker='+-')
    # ax1.set_xlim([0, this.bins])
    ax1.set_xticks([0, this.bins / 4, this.bins /
                    2, 3 * this.bins / 4, this.bins])
    ax1.set_xticklabels(
        [r'$-\pi$', r'$-\frac{1}{2}\pi{}$', r'$0$', r'$\frac{1}{2}\pi$', r'$\pi$'])
    ax1.set_xlabel(r'$\theta$ (rad)')
    ax1.set_ylabel('Flux $J$ (cycle s$^{-1}$)')
    ax1.legend(frameon=True, loc=1, framealpha=1.0, edgecolor='k')
    paper_plot(fig, scientific=False)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')


def plot_load(this, save=False, filename=None):
    """
    This function plots the unbound and bound energy surfaces with a constant added load.
    """

    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax1.plot(range(this.bins), [this.unbound_energy[i] + this.load_function(i) for i in range(this.bins)],
             c='k', ls='--', lw=2)
    ax1.plot(range(this.bins), this.unbound_energy, c=this.unbound_clr)
    ax1.plot(range(this.bins), [this.bound_energy[i] + this.load_function(i) for i in range(this.bins)],
             c='k', ls='--', lw=2)
    ax1.plot(range(this.bins), this.bound_energy, c=this.bound_clr, ls='--')

    ax1.set_xticks([0, this.bins / 4, this.bins /
                    2, 3 * this.bins / 4, this.bins])
    ax1.set_xticklabels(
        [r'$-\pi$', r'$-\frac{1}{2}\pi{}$', r'$0$', r'$\frac{1}{2}\pi$', r'$\pi$'])
    ax1.set_xlabel(r'$\theta$ (rad)')
    ax1.set_ylabel(r'Free energy (kcal mol$^{-1}$)')
    paper_plot(fig, scientific=False)
    if save:
        plt.savefig(filename + '.png', dpi=300, bbox_inches='tight')


def plot_fluxes_and_velocity(concentrations, directional_flux, reciprocating_flux, velocity,
                             ymin1=None, ymax1=None, label=None):
    """

    :param concentrations:
    :param directional_flux:
    :param reciprocating_flux:
    :param velocity:
    :param ymin1:
    :param ymax1:
    :param label:
    """
    cmap = sns.color_palette("Paired", 10)
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])

    ax1.plot(concentrations, velocity, c=cmap[1])
    ax1.set_xscale('log')
    ax1.set_ylim([ymin1, ymax1])
    ax1.set_ylabel(r'Catalytic rate (turnover s$^{{-1}}$)', color=cmap[1])

    ax2 = ax1.twinx()
    ax2.plot(concentrations, [abs(i) for i in directional_flux], c=cmap[3])
    ax2.plot(concentrations, [abs(i)
                              for i in reciprocating_flux], c=cmap[3], ls='--')
    ax2.set_ylabel('Flux (cycle s$^{{-1}}$)', color=cmap[3])
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
    if label:
        ax.annotate(r'{}'.format(label), xy=(0.5, 0.5), xytext=(
            0.18, 0.70), xycoords='figure fraction', fontsize=20)
    threshold_labels = ['Directional', 'Reciprocating']
    linestyles = ['-', '--']
    colors = [cmap[3], cmap[3]]
    handles, labels = ax.get_legend_handles_labels()
    display = (0, 1, 2)
    artists = []
    if threshold_labels:
        for threshold_label, style, c in zip(threshold_labels, linestyles, colors):
            artists.append(plt.Line2D(
                (0, 1), (0, 0), color=c, linestyle=style))
        ax.legend([handle for i, handle in enumerate(handles) if i in display] + artists,
                  [label for i, label in enumerate(
                      labels) if i in display] + threshold_labels,
                  loc='upper left', frameon=True, framealpha=1.0, edgecolor='k')
    ax1.set_xlim([10 ** -6, 10 ** 0])
    ax1.set_xticks([10 ** -6, 10 ** -5, 10 ** -4,
                    10 ** -3, 10 ** -2, 10 ** -1, 10 ** 0])
    fig.patch.set_facecolor('white')


def plot_directional_flux_and_velocity(concentrations, directional_flux, velocity,
                                       ymin1=None, ymax1=None, label=None):
    """

    :param concentrations:
    :param directional_flux:
    :param reciprocating_flux:
    :param velocity:
    :param ymin1:
    :param ymax1:
    :param label:
    """
    cmap = sns.color_palette("Paired", 10)
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax1 = plt.subplot(gs[0, 0])

    ax1.plot(concentrations, velocity, c=cmap[1])
    ax1.set_xscale('log')
    ax1.set_ylim([ymin1, ymax1])
    ax1.set_ylabel(r'Catalytic rate (turnover s$^{{-1}}$)', color=cmap[1])

    ax2 = ax1.twinx()
    ax2.plot(concentrations, [abs(i) for i in directional_flux], c=cmap[3])
    ax2.set_ylabel('Directional flux (cycle s$^{{-1}}$)', color=cmap[3])
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
    if label:
        ax.annotate(r'{}'.format(label), xy=(0.5, 0.5), xytext=(
            0.18, 0.88), xycoords='figure fraction', fontsize=20)
    ax1.set_xlim([10 ** -6, 10 ** 0])
    ax1.set_xticks([10 ** -6, 10 ** -5, 10 ** -4,
                    10 ** -3, 10 ** -2, 10 ** -1, 10 ** 0])
    fig.patch.set_facecolor('white')


def plot_flux_over_threshold(concentrations, number_above_thresholds, colors, names,
                             threshold_labels=None, xmin=10 ** -6, xmax=10 ** -2, ymin=0, ymax=140):
    """

    :param concentrations:
    :param number_above_thresholds:
    :param colors:
    :param names:
    :param threshold_labels:
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    """
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax = plt.subplot(gs[0, 0])
    linestyles = ['-', '--']
    # For simplicity, I think I should enforce paired plotting. That is, to plot the number of angles over two
    # thresholds for each system, with the line styles given above. We should be able to handle an arbitrary number of
    # pairs.
    pairs = [number_above_thresholds[x:x + 2]
             for x in range(0, len(number_above_thresholds), 2)]
    for system, color, name in zip(pairs, colors, names):
        ax.plot(concentrations, system[0], ls='-', c=color, label=name)
        ax.plot(concentrations, system[1], ls='--', c=color)

    handles, labels = ax.get_legend_handles_labels()
    display = (0, 1, 2)
    artists = []
    if threshold_labels:
        for threshold_label, style in zip(threshold_labels, linestyles):
            artists.append(plt.Line2D(
                (0, 1), (0, 0), color='k', linestyle=style))

        ax.legend([handle for i, handle in enumerate(handles) if i in display] + artists,
                  [label for i, label in enumerate(
                      labels) if i in display] + threshold_labels,
                  loc='upper left', frameon=True, framealpha=1.0, edgecolor='k')
    ax.set_xlabel('Substrate concentration (M)')
    ax.set_ylabel('Number over threshold')
    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    paper_plot(fig)


def plot_load_over_threshold(concentrations, number_above_thresholds, colors, names,
                             annotation=None, annotation_x=None, annotation_y=None,
                             xmin=10 ** -6, xmax=10 ** -2, ymin=0, ymax=140):
    """

    :param concentrations:
    :param number_above_thresholds:
    :param colors:
    :param names:
    :param annotation:
    :param annotation_x:
    :param annotation_y:
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    """
    fig = plt.figure(figsize=(6 * 1.2, 6))
    gs = GridSpec(1, 1, wspace=0.2, hspace=0.5)
    ax = plt.subplot(gs[0, 0])

    for system, color, name in zip(number_above_thresholds, colors, names):
        ax.step(concentrations, system, ls='-', c=color, label=name)

    if annotation:
        ax.annotate(annotation, xy=(0.5, 0.5),
                    xytext=(annotation_x, annotation_y), xycoords='figure fraction', fontsize=20)

    ax.legend(loc='upper left', frameon=True, framealpha=1.0, edgecolor='k')
    ax.set_xlabel('Substrate concentration (M)')
    ax.set_ylabel('Number over threshold')
    ax.set_xscale('log')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    paper_plot(fig)


# Below, these helper functions are necessary for the summary plots that are designed mostly to read in pandas
# dataframes
def return_concentration_slice(df, concentration):
    """
    This helper function makes slicing dataframes easy.
    :param df: a dataframe that contains a column named 'Concentration'
    :param concentration: a target concentration, that will be rounded
    :return: the dataframe slice at the given concentration
    """
    tmp = df[np.round(df['Concentration'], 1) == np.round(concentration, 1)]
    return tmp


def return_fluxes_and_velocity(protein, name, concentrations, catalytic_rate=None,
                               directory=None):
    """
    This helper function will return the turnover rate and the fluxes over a concentration range.
    :param protein: one of the recognized protein systems in the class
    :param name: filename of the torsion
    :param concentrations: a list concentrations
    :return:
    """
    directional_flux, reciprocating_flux, velocity = [], [], []
    for concentration in concentrations:
        this = Simulation(data_source=protein)
        this.name = name
        this.cSubstrate = concentration
        if catalytic_rate:
            this.catalytic_rate = catalytic_rate
        this.simulate(directory=directory)
        directional_flux.append(np.mean(this.flux_u + this.flux_b))
        reciprocating_flux.append(
            np.max(np.hstack((abs(this.flux_u), abs(this.flux_b)))))
        velocity.append(
            np.sum(this.ss[this.bins:2 * this.bins]) * this.catalytic_rate)
    return directional_flux, reciprocating_flux, velocity


def find_above_threshold(df, quantity, threshold):
    """

    :param df:
    :param quantity:
    :param threshold:
    :return:
    """
    concentrations = []
    number_above_threshold = []
    for concentration in tqdm(np.unique(df['Concentration'].values)):
        tmp = return_concentration_slice(df, concentration)
        concentrations.append(10 ** concentration)
        number_above_threshold.append(
            sum(tmp[str(quantity)].abs() > threshold))
    return concentrations, number_above_threshold


def data_frame_to_chimera(df, df_index_column, df_target_column, filename, chimera_label):
    """

    :param df:
    :param df_index_column:
    :param df_target_column:
    :param filename:
    :param chimera_label:
    """
    file = str(filename) + '.dat'
    f = open(file, 'w')
    f.write('attribute: {}\n'.format(chimera_label))
    f.write('match mode: any\n')
    f.write('recipient: residues\n')
    for i in range(min(df[df_index_column].astype(int)), max(df[df_index_column].astype(int)) + 1):
        x = np.max(abs(df[df[df_index_column] == i][df_target_column]))
        f.write('\t:{}\t{}\n'.format(i, x))
    f.close()


if __name__ == "__main__":
    prepare_plot()
