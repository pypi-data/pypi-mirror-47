# cython: infer_types=True

cimport cython
import numpy as np
cimport numpy as np
from cython.parallel import prange

np.import_array()

# DTYPE = np.int
# ctypedef np.int_t DTYPE_t

# cpdef np_count(np.ndarray[DTYPE_t, ndim=1, mode='c'] arr):
#     print('1111111')
    # c = (arr == value).sum()
    #
    # if default is not None and c == 0:
    #     return default
    #
    # return c

# cdef int np_count(int n):
#     cdef int i, r
#     for i in range(n):
#         r += i
#     return i
#
# def test_loop(n):
#     return np_count(n)


cdef c_min(double[:] arr):
    cdef double res = np.inf

    for i in range(arr.shape[0]):
        if res > arr[i]:
            res = arr[i]
    return res


cdef c_sum_axis_0(double[:,:] arr):
    cdef double[:] res = np.zeros(arr.shape[1], dtype=np.float)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            res[j] += arr[i, j]

    return res

cdef c_sum_axis_1(double[:,:] arr):
    cdef double[:] res = np.zeros(arr.shape[0], dtype=np.float)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            res[i] += arr[i, j]

    return res


# cdef c_sum_axis_0(np.ndarray[np.float_t, ndim=2] arr):
#     cdef np.PyArrayObject *res
#     np.PyArray_Sum(arr, 0, 0, res)
#     return *res



cdef c_sum(double[:,:] arr):
    cdef double res = 0

    cdef Py_ssize_t i,j
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            res += arr[i, j]

    return res




#
# feature = np.random.rand(500)
#
# np_count(feature)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef ChiMerge_c(feature, target, n_bins = 20, min_samples = None,
            min_threshold = None, nan = -1, balance = True):
    """Chi-Merge

    Args:
        feature (array-like): feature to be merged
        target (array-like): a array of target classes
        n_bins (int): n bins will be merged into
        min_samples (number): min sample in each group, if float, it will be the percentage of samples
        min_threshold (number): min threshold of chi-square

    Returns:
        array: array of split points
    """

    target_unique = np.unique(target)
    feature_unique = np.unique(feature)
    len_f = len(feature_unique)
    len_t = len(target_unique)

    cdef double [:,:] grouped = np.zeros((len_f, len_t))

    for r in range(len_f):
        tmp = target[feature == feature_unique[r]]
        for c in range(len_t):
            grouped[r, c] = (tmp == target_unique[c]).sum()


    cdef double [:,:] couple
    cdef double [:] cols, rows, chi_list
    # cdef long [:] min_ix, drop_ix
    # cdef long[:] chi_ix
    cdef double chi, chi_min, total, e
    cdef int l, retain_ix, ix
    cdef Py_ssize_t i, j, k, p

    while(True):
        # break loop when reach n_bins
        if n_bins and len(grouped) <= n_bins:
            break

        # break loop if min samples of groups is greater than threshold
        if min_samples and c_min(c_sum_axis_1(grouped)) > min_samples:
            break

        # Calc chi square for each group
        l = len(grouped) - 1
        chi_list = np.zeros(l)
        chi_min = np.inf
        # chi_ix = []
        for i in range(l):
            chi = 0
            couple = grouped[i:i+2,:]
            total = c_sum(couple)
            cols = c_sum_axis_0(couple)
            rows = c_sum_axis_1(couple)

            for j in range(couple.shape[0]):
                for k in range(couple.shape[1]):
                    e = rows[j] * cols[k] / total
                    if e != 0:
                        chi += (couple[j, k] - e) ** 2 / e

            # balance weight of chi
            if balance:
                chi *= total

            chi_list[i] = chi

            if chi == chi_min:
                chi_ix.append(i)
                continue

            if chi < chi_min:
                chi_min = chi
                chi_ix = [i]

            # if chi < chi_min:
            #     chi_min = chi




        # break loop when the minimun chi greater the threshold
        if min_threshold and chi_min > min_threshold:
            break

        # get indexes of the groups who has the minimun chi
        min_ix = np.array(chi_ix)
        # min_ix = np.where(chi_list == chi_min)[0]

        # get the indexes witch needs to drop
        drop_ix = min_ix + 1


        # combine groups by indexes
        retain_ix = min_ix[0]
        last_ix = retain_ix
        for ix in min_ix:
            # set a new group
            if ix - last_ix > 1:
                retain_ix = ix

            # combine all contiguous indexes into one group
            for p in range(grouped.shape[1]):
                grouped[retain_ix, p] = grouped[retain_ix, p] + grouped[ix + 1, p]

            last_ix = ix


        # drop binned groups
        grouped = np.delete(grouped, drop_ix, axis = 0)
        feature_unique = np.delete(feature_unique, drop_ix)


    return feature_unique[1:]



def _ChiMerge(feature, target, n_bins = 20, min_samples = None,
            min_threshold = None, nan = -1, balance = True):

    return ChiMerge_c(
        feature,
        target,
        n_bins = n_bins,
        min_samples = min_samples,
        min_threshold = min_threshold,
        nan = nan,
        balance = balance,
    )
