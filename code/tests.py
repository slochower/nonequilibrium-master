import unittest
import logging
from simulation import *
from models import *

class equilibrium(unittest.TestCase):

    def test_flux_is_zero_with_no_potential(self):
        bins = np.random.randint(0, 100)
        this = simulation()
        this.unbound = flat(bins)
        this.bound = flat(bins)
        this.catalytic_rate = 0
        this.simulate()
        flux = np.mean(this.flux_u + this.flux_b)
        self.assertAlmostEqual(flux, 0, places=2, msg='Flux is nonzero for zero potential surface.')

    def test_flux_is_zero_with_random_potential(self):
        bins = np.random.randint(0, 100)
        this = simulation()
        this.unbound = np.random.rand(bins)
        this.bound = np.random.rand(bins)
        this.unbound /= np.sum(this.unbound)
        this.bound /= np.sum(this.bound)
        this.catalytic_rate = 0
        this.simulate()
        flux = np.mean(this.flux_u + this.flux_b)
        self.assertAlmostEqual(flux, 0, places=2, msg='Flux is nonzero for random potential surface.')

    def test_maximum_eigenvalue_is_1(self):
        bins = np.random.randint(0, 100)
        this = simulation()
        this.unbound = flat(bins)
        this.bound = flat(bins)
        this.catalytic_rate = 0
        this.simulate()
        maximum_eigenvalue = this.eigenvalues[this.eigenvalues.argmax()]
        self.assertAlmostEqual(maximum_eigenvalue, 1, places=7, msg='Maximum eigenvalue is not 1.')

    def test_ss_is_boltzmann(self):
        bins = 4
        this = simulation()
        this.unbound = np.random.rand(bins)
        this.bound = np.random.rand(bins)
        this.unbound /= np.sum(this.unbound)
        this.bound /= np.sum(this.bound)
        this.catalytic_rate = 0
        this.offset_factor = 0  # Both surfaces should have equal probability
        this.cSubstrate = 1

        this.ss[bins:] /= this.ss[bins:]

        this.simulate()
        unbound_difference = abs(this.ss[0:bins]) - abs(this.PDF_unbound)
        bound_difference = abs(this.ss[bins:]) - abs(this.PDF_bound)
        difference = np.sum(unbound_difference) + np.sum(bound_difference)
        self.assertAlmostEqual(difference, 0, places=3, msg='Steady state differs from Boltzmann in equilibrium.')


def main():
    unittest.main()

if __name__ == '__main__':
    # Turn on logging for specific tests.
    main()