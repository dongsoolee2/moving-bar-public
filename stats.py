"""
Statistics functions to analyze retinal physiology data
"""

import numpy as np
import itertools
import scipy.stats

__all__ = ['mean', 'corr', 'corr_pair', 'corr_mean', 'pearsonr_mask']

def mean(arr, axis=0, use_half_trial=0):
    D = arr.ndim
    if D == 4:
        _, _, N, _ = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:, :, :N, :]
    elif D == 3:
        _, N, _ = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:, :N, :]
    elif D == 2:
        N, _ = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:N, :]
    return np.nanmean(arr, axis=axis)


def corr(arr, mode='pair', use_half_trial=0):
    D = arr.ndim
    if D == 4:
        D1, D2, N, T = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:, :, :N, :]
        if mode == 'pair':
            C = int(N * (N - 1) / 2)
            result = np.zeros((D1, D2, C, 2))
            for d1 in range(D1):
                for d2 in range(D2):
                    result[d1, d2, :, :] = corr_pair(arr[d1, d2, :, :])
            return result
        elif mode == 'mean':
            result = np.zeros((D1, D2, N, 2))
            for d1 in range(D1):
                for d2 in range(D2):
                    result[d1, d2, :, :] = corr_mean(arr[d1, d2, :, :])
            return result
    elif D == 3:
        D1, N, T = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:, :N, :]
        if mode == 'pair':
            C = int(N * (N - 1) / 2)
            result = np.zeros((D1, C, 2))
            for d1 in range(D1):
                result[d1, :, :] = corr_pair(arr[d1, :, :])
            return result
        elif mode == 'mean':
            result = np.zeros((D1, N, 2))
            for d1 in range(D1):
                result[d1, :, :] = corr_mean(arr[d1, :, :])
            return result
    elif D == 2:
        N, T = arr.shape
        if use_half_trial:
            N = int(N/2)
            arr = arr[:N, :]
        if mode == 'pair':
            return corr_pair(arr)
        elif mode == 'mean':
            return corr_mean(arr)

def corr_pair(arr):
    N, T = arr.shape
    C = int(N * (N - 1) / 2)
    result = np.zeros((C, 2))
    for i, (a, b) in enumerate(itertools.combinations(range(N), 2)):
        cc, p = pearsonr_mask(arr[a, :], arr[b, :])
        result[i, 0] = cc
        result[i, 1] = p
    return result

def corr_mean(arr):
    N, T = arr.shape
    arr_mean = np.nanmean(arr, axis=0)
    result = np.zeros((N, 2))
    for i in range(N):
        cc, p = pearsonr_mask(arr[i, :], arr_mean)
        result[i, 0] = cc
        result[i, 1] = p
    return result

def pearsonr_mask(a, b):
    mask = np.logical_or(np.isnan(a), np.isnan(b))
    return scipy.stats.pearsonr(a[~mask], b[~mask])
