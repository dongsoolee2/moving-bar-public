"""
Functions to analyze retinal physiology data
"""

import numpy as np
import scipy.signal
import pyret.stimulustools as st

__all__ = ['ts2st', 'mb_roll', 'i_downsample']

def ts2st(arr):
    return arr[:, ::-1].T

def mb_roll(arr, shift=(0, 0), padding=70, pad_mode='constant'):
    if np.isnan(arr).shape == ():
        return np.nan
    else:
        if np.sum(np.isnan(shift)) > 0:
            shift = (0, 0)
        padder = ((0, 0), (0, 0), (0, 0), (padding, padding))
        arr_pad = np.pad(arr, pad_width=padder, mode=pad_mode)
        arr_pad_l = arr_pad[0]
        arr_pad_r = arr_pad[1]
        arr_pad_l_s = np.roll(arr_pad_l, int(shift[0]), axis=2)
        arr_pad_r_s = np.roll(arr_pad_r, int(shift[1]), axis=2)
        arr_pad_s = np.stack([arr_pad_l_s, arr_pad_r_s])[:, :, :, padding:-padding]
        return arr_pad_s

def i_downsample(arr, num_sample):
    if np.isnan(arr).shape == ():
        return np.nan
    else:
        N = arr.ndim
        if N == 4:
            D1, D2, trial, _ = arr.shape
            arr_ds = np.zeros((D1, D2, trial, num_sample))
            for d1 in range(D1):
                for d2 in range(D2):
                    for t in range(trial):
                        arr_ds[d1, d2, t, :] = scipy.signal.resample(st.downsample(arr[d1, d2, t, :], 10)[0], num_sample)
            return arr_ds
        else:
            return arr


