import numpy as np


def saw(x, a):
    """Return a sawtooth wave, specified by the position and period."""
    return 2 * (x / a - np.floor(1 / 2 + x / a))


def variable_saw(y, x, a):
    """Return a sawtooth wave, specified by the position and period, with a
    mangitude parameter."""
    return y * (x / a - np.floor(1 / 2 + x / a))


def generate_candidates(low, high, bins):
    """Generate some candidate load functions within some parameter space."""
    load = np.linspace(low, high, bins)
    return load


def flat(bins):
    """Return a flat landscape with specified number of bins."""
    return [0] * bins
