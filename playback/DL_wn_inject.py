# DL_wn_inject(recorded file *.h5, threshold, interval)

# DL_wn_inject function calculates current to be injected
# to compute transmission filter from recorded cell to ganglion cells.
#
# by Dongsoo Lee (created 18-03-07, edited 18-00-00)


import numpy as np
import scipy.signal
import h5py
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b_l, a_l = butter(order, normal_cutoff, btype='low', analog=False)
    return b_l, a_l


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b_l, a_l = butter_lowpass(cutoff, fs, order=order)
    y_l = filtfilt(b_l, a_l, data)
    # filtfilt is to compensate delay introduced by this lowpass filter
    return y_l


# parameters
# -----------------------------------------------------------
fileName = "/home/dsnl/wn"
fileTag = ".h5"
file_r = fileName + fileTag
order_l = 4 		# order of the lowpass filter
cutoff_l = 50	#15	# desired cutoff frequency of the lowpass filter, [Hz]
fs = 10000.0  		# sampling rate, [Hz]
# -----------------------------------------------------------


# Generate random number from standard normal distribution
np.random.seed(0)
wn_sequence = np.random.standard_normal(3000000)
wn_sequence_lf = butter_lowpass_filter(wn_sequence, cutoff_l, fs, order_l)
wn_sequence_lf[:100] = 0    				# to deal with artifact
wn_current = wn_sequence_lf/np.std(wn_sequence_lf)*0.5	# std of current = 0.5 (500 pA)


# Create a new hdf5 file for injection
analogoutput = "-ao"
wn_500 = "-500"
file_wn_500 = fileName + wn_500 + analogoutput + fileTag


# Write
f_w_wn = h5py.File(file_wn_500, 'w')
dset_wn = f_w_wn.create_dataset('analog-output', (np.size(wn_current),), dtype='double', data=wn_current)
f_w_wn.close()

