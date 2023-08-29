# DL_rfmap(recorded file *.h5, threshold, interval)
#
# DL_rfmap function calculates receptive field of checker board stimulus
#
# by Dongsoo Lee (created 17-07-18, edited 17-00-00)


import numpy as np
import h5py
import scipy.io
import scipy.signal
import matplotlib.pyplot as plt
import pyret.spiketools
from pyret.filtertools import revcorr
from pyret.stimulustools import upsample, downsample


# parameter
M = 80  # kernel length

# Load output
fileName = "/home/dsnl/rf.h5"
f = h5py.File(fileName, 'r')
gain = np.double(f['data'].attrs['gain'])
# offset = f['data'].attrs['offset']
offset = 0
voltage_raw = (-np.double(f['data'][1, :]) * gain - offset) * 0.1  # [V]

# get the last flip from photodiode reference
photodiode = np.double(f['data'][0, :]) * gain - offset
max_value = np.max(photodiode)
photodiode_norm = photodiode / max_value
threshold = 0.9
maxtab, mintab = pyret.spiketools.peakdet(photodiode_norm, threshold)
print(maxtab)
f.close()

# Load input
mat = scipy.io.loadmat('/home/dsnl/boxColor_w8.mat')
stim = mat['boxColor'][0, :, :9000]
stim = stim.reshape(32, 32, 9000)
stim = np.einsum('ijk->kji', stim)
#stim = np.einsum('ij->ji', stim)

# Downsample the voltage
voltage_down = downsample(voltage_raw[np.int(maxtab[1, 0]):np.int(maxtab[2, 0])], 100)[0]

# upsample the stimulus
stim_us = upsample(stim, 6)[0]

# resample the voltage
voltage_rs = scipy.signal.resample(voltage_down, np.size(stim_us, 0))

# reconstruct input & output
input_stim = stim_us - np.mean(stim_us)
output = voltage_rs - np.mean(voltage_rs)


# calculate reverse correlation
rc, rags = revcorr(input_stim, output[M-1:], M)  ####### 

#aaaaaaaaaaaaaaaaaaa stim
####aaaaaaaaaaaaaaaa output

# subtract mean
line_rf = rc - np.mean(rc, axis=0)

# plot
plt.imshow(line_rf[63, :, :])
#plt.imshow(rc[63, :, :])
plt.show()

#plt.plot(line_rf[:, 15, 12])
#plt.show()
