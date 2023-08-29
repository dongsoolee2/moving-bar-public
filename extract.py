"""
Tools to extract data (from raw data) temporally aligned with respect to visual
stimulus
"""
import numpy as np
import scipy.io
import h5py
import warnings


__all__ = ['txt2array', 'photodiode', 'electrode', 'split_trial', 'select_trial',
        'load_stimulus']


def txt2array(path, N):
    cell_array = []
    for num in range(1, N + 1):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cell_array.append(np.loadtxt(path + 'c' + str('%.2d' %num) +
                '.txt'))
    return cell_array

def photodiode(path, ch=0, key=None):
    value, gain, offset = _channel(path, ch, key)
    value -= np.min(value)
    value /= np.max(value)
    return value

def electrode(path, ch=1, key=None):
    value, gain, offset = _channel(path, ch, key)
    electrode2DAQ = np.polyfit([-100, -10, 0, 10, 100],
            [6297.0, 708.9, 104.5, -555.4, -6108.9], 1)     # measured on Feb 27th, 2019
    g = lambda y: (y - electrode2DAQ[1]) / electrode2DAQ[0]
    elect = g(value)
    return elect

def _channel(path, ch, key=None):
    with h5py.File(path, 'r') as f:
        if key == None:
            key = list(f.keys())[0]
        gain = np.double(f[key].attrs['gain'])
        offset = np.double(f[key].attrs['offset'])
        value = np.double(f[key][ch, :])
    return value, gain, offset

def split_trial(array, maxtab, start, last, every, per=1, sample_rate=10000.0,
        mode='continuous'):
    sublist = []
    if mode == 'continuous':
        for trial in range(start, last, every):
            idx1 = np.int(maxtab[trial, 0])
            idx2 = np.int(maxtab[trial + per, 0])
            sublist.append(array[idx1:idx2])
    elif mode == 'discrete':
        g = lambda x, idx1, idx2: x[(x >= idx1) & (x < idx2)]
        for trial in range(start, last, every):
            idx1 = maxtab[trial, 0] / sample_rate
            idx2 = maxtab[trial + per, 0] / sample_rate
            sublist.append(g(array, idx1, idx2) - idx1)
    else:
        print("mode should be either 'continuous' or 'discrete'")
    return sublist

def list_to_array(li, ndim=1):
    max_idx = 0
    for i in range(len(li)):
        if max_idx < li[i].shape[-1]:
            max_idx = li[i].shape[-1]
    array = np.full((len(li),) + li[0].shape[:-1] + (max_idx,), np.nan)
    if ndim == 1:
        for i in range(len(li)):
            array[i, :li[i].shape[0]] = li[i]
    return array

def select_trial(sublist, select=1, mode='mono'):
    sublist_tmp = []
    if mode == 'mono':
        sublist_tmp = sublist[select]
    elif mode == 'binary':
        sublist_tmp = [sublist[i] for i in select]
    elif mode == 'multi':
        sublist_tmp = sublist # to be completed
    return sublist_tmp

def reorder_trial():
    pass

def load_stimulus(path, mode='mono', two_dim=True):
    dir_path = '/Users/dlee/moving-bar/matrix/'
    if path == '2d_st_bin_wn_w8':
        file_path = dir_path + 'boxColor_w8.mat'
        two_dim = True
    elif path == '1d_st_bin_wn_w4':
        file_path = dir_path + 'lineColor_w4.mat'
        two_dim = False
    elif path == '1d_st_bin_wn_w8':
        file_path = dir_path + 'lineColor_w8.mat'
        two_dim = False
    else:
        file_path = path
    mat = scipy.io.loadmat(file_path)
    stim = mat[sorted(mat.keys())[-1]].swapaxes(2, 1)
    T = stim.shape[1]
    xx = stim.shape[2]
    x = np.int(np.sqrt(xx))
    if two_dim:
        stim = stim.reshape(-1, T, x, x)
    if mode == 'mono':
        stim = stim[0]
    return np.double(stim)

def load_stimulus_mb():
    mb = np.zeros((129, 256))
    for time in range(0, mb.shape[0]):
        if 2*time - 24 < 0:
            mb[time, : 2*time] = -0.5
        else:
            mb[time, 2*time - 24 : 2*time] = -0.5
    return mb
