"""
General functions to help analyze retinal physiology data
"""

import numpy as np
import scipy.signal
import h5py
import matplotlib
import matplotlib.pyplot as plt

__all__ = ['h5view', 'file_name', 'split_half_nan', 'butter_lowpass_filter',
        'butter_highpass_filter', 'color_index', 'set_plot_params']

def h5view(path):
    with h5py.File(path, "r") as f:
        print("key():")
        for key in list(f.keys()):
            print("\t '{}'".format(key))
            print("\t\t", "shape: ", f[key].shape)
            print("\t\t", "attrs:")
            for att in list(f[key].attrs.keys()):
                print("\t\t\t '{}':\t{}".format(att, f[key].attrs[att]))

def file_name(date, retina_idx, intracell_idx, exp_type):
    retina_name = 'r' + str(retina_idx)
    intracell_name = 'c' + str(intracell_idx)
    if exp_type == 'flash_1':
        return '-'.join([date, retina_name, intracell_name, '0', 'flash']) + '.h5'
    elif exp_type == 'mb_ns':
        return '-'.join([date, retina_name, intracell_name, '4', 'mb', 'ns']) + '.h5'
    elif exp_type == 'mb_ad':
        return '-'.join([date, retina_name, intracell_name, '5', 'mb', 'ad']) + '.h5'
    elif exp_type == 'mb_da':
        return '-'.join([date, retina_name, intracell_name, '6', 'mb', 'da']) + '.h5'
    elif exp_type == 'mb_2ad':
        return '-'.join([date, retina_name, intracell_name, '7', 'mb', '2ad']) + '.h5'
    elif exp_type == 'mb_2da':
        return '-'.join([date, retina_name, intracell_name, '8', 'mb', '2da']) + '.h5'
    elif exp_type == 'mb_4ad':
        return '-'.join([date, retina_name, intracell_name, '7', 'mb', '4ad']) + '.h5'
    elif exp_type == 'mb_4da':
        return '-'.join([date, retina_name, intracell_name, '8', 'mb', '4da']) + '.h5'
    elif exp_type == 'rf_30m':
        return '-'.join([date, retina_name, 'rf']) + '.h5'
    elif exp_type == 'rf_wn':
        return '-'.join([date, retina_name, intracell_name, '2', 'rf', 'wn']) + '.h5'
    elif exp_type == 'line_w4':
        return '-'.join([date, retina_name, intracell_name, '1', 'line']) + '.h5'
    elif exp_type == 'line_w8':
        return '-'.join([date, retina_name, intracell_name, '1', 'line']) + '.h5'
    elif exp_type == 'rf_5m':
        return '-'.join([date, retina_name, intracell_name, '2', 'rf']) + '.h5'
    elif exp_type == 'mb':
        return '-'.join([date, retina_name, intracell_name, '3', 'mb']) + '.h5'
    elif exp_type == 'flash_2':
        return '-'.join([date, retina_name, intracell_name, '9', 'flash']) + '.h5'
    elif exp_type == 'mb_ad_ao':
        return '-'.join([intracell_name, 'mb', 'ad', 'ao']) + '.h5'
    elif exp_type == 'wn_500_ao':
        return '-'.join(['wn', '500', 'ao']) + '.h5'
    else:
        print("Check your file name!")

def split_half_nan(arr, use_half_trial=0):
    if use_half_trial:
        D = arr.ndim
        if D == 4:
            _, _, N, _ = arr.shape
            N = int(N/2)
            arr[:, :, N:, :] = np.nan
        elif D == 3:
            _, N, _ = arr.shape
            N = int(N/2)
            arr[:, N:, :] = np.nan
        elif D == 2:
            N, _ = arr.shape
            N = int(N/2)
            arr[N:, :] = np.nan
        return arr
    else:
        return arr

def butter_lowpass_filter(data, cutoff=15, fs=10000.0, order=4):
    b_l, a_l = _butter_lowpass(cutoff, fs, order=order)
    y_l = scipy.signal.filtfilt(b_l, a_l, data)
    # filtfilt is to compensate delay introduced by this lowpass filter
    return y_l

def _butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b_l, a_l = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b_l, a_l

def butter_highpass_filter(data, cutoff=0.04, fs=10000.0, order=3):
    b_h, a_h = _butter_highpass(cutoff, fs, order=order)
    y_h = scipy.signal.filtfilt(b_h, a_h, data)
    return y_h

def _butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b_h, a_h = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b_h, a_h

def color_index():
    color_code = ['#E6194B', '#3CB44B', '#FFE119', '#0082C8',
            '#F58231', '#911EB4', '#46F0F0', '#F032E6',
            '#D2F53C', '#FABEBE', '#008080', '#E6BEFF',
            '#AA6E28', '#800000', '#AAFFC3', '#808000',
            '#FFD8B1', '#000080', '#808080', '#FFFAC8']
    return color_code

def set_plot_params():
    plt.rcParams['figure.figsize'] = [4.0, 2.0]
  #  plt.rcParams['figure.autolayout'] = True
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 12

    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.markersize'] = 2
    plt.rcParams['axes.linewidth'] = 0.7
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['ytick.major.size'] = 3

