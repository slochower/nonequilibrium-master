from simulation import *
from aesthetics import *
from plot import *

# Figure 1
directory = './figure1/'
prepare_plot()

this = Simulation(data_source = 'adk_md_data')
this.name = 'chi2THR175'  # Name of torsion
this.cSubstrate = 10**-3  # Substrate concentration in [M]
this.simulate()

plot_input(this)
ax = plt.gca()
names=['Apo', 'Bound']
ax.legend(names, frameon=True, loc='upper right', edgecolor='k', framealpha=1.0)
ax.set_ylabel('Equilibrium population density')
ax.set_xlabel('')
panel_label('b', panel_xoffset=-0.23, panel_yoffset=1.0)
plt.savefig(directory + '1b.png', dpi=fig.dpi)
plt.savefig(directory + '1b.pdf')

plot_energy(this)
ax = plt.gca()
ax.set_ylabel('Free energy (kcal mol$^{{-1}}$)')
panel_label('c', panel_xoffset=-0.2, panel_yoffset=1.0)
plt.savefig(directory + '1c.png', dpi=fig.dpi)
plt.savefig(directory + '1c.pdf')

plot_flux(this)
ax = plt.gca()
ax.set_ylim([-200, 50])
panel_label('d', panel_xoffset=-0.23, panel_yoffset=1.0)
plt.savefig(directory + '1d.png', dpi=fig.dpi)
plt.savefig(directory + '1d.pdf')

# Figure 2

# Figure 3

# Figure 4
