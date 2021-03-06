import numpy as np


def calculate_sigma_points(states, flat_covs, scaling_factor, out,
                           square_root_filters):
    """Calculate the array of sigma_points for the unscented transform.

    Args:
        states (np.ndarray): numpy array of (nind, nemf, nfac)
        flat_covs (np.ndarray): numpy array of (nind * nemf, nfac, nfac)
        scaling_factor (float): a constant scaling factor for sigma points that
            depends on the sigma_point algorithm chosen.
        out (np.ndarray): numpy array of (nemf * nind, nsigma, nfac) with
            sigma_points.
        square_root_filters (bool): indicates if square-root filters are used.

    """
    if square_root_filters is True:
        cholcovs_t = flat_covs[:, 1:, 1:]
    else:
        cholcovs_t = np.transpose(np.linalg.cholesky(flat_covs),
                                  axes=(0, 2, 1))

    nemf_times_nind, nsigma, nfac = out.shape
    out[:] = states.reshape(nemf_times_nind, 1, nfac)
    cholcovs_t *= scaling_factor
    out[:, 1: nfac + 1, :] += cholcovs_t
    out[:, nfac + 1:, :] -= cholcovs_t
