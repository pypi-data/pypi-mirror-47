import numpy as np
import numexpr as ne

def PDF(pos, nb_samples, rcut, bin_count):
    """
    Pair Distribution Function. Returns normalized histogram of distance between atoms.

    Parameters
    ----------
    pos : np.array
        Array containing atoms position
    nb_samples : int
        Number of atoms from which to generate the histogram
    rcut : number
        Maximum distance to consider
    bin_count : int
        Number of bins of the histogram

    Returns
    -------
    bins, hist : tuple(np.array, np.array)
        `bins` being the distances, `hist` the normalized (regarding radius) histogram

    """
    bins = np.linspace(0, rcut, bin_count)
    samples = np.random.choice(range(len(pos)), nb_samples)
    hist = np.zeros(len(bins)-1)
    for s in samples:
        sample = pos[s,:]
        dists = np.array([a for a in np.sqrt(ne.evaluate("sum((pos-sample)**2,axis=1)")) if a])
        hist += np.histogram(dists, bins=bins, weights=1/dists)[0]
    return bins[:-1], hist/nb_samples
