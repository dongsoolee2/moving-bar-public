# DL_pulse_inject()

# DL_pulse_inject function calculates current to be injected
# for neurobiotin staining.
#
# by Dongsoo Lee (created 18-04-12, edited 18-00-00)


import numpy as np
import scipy.signal
import h5py
import matplotlib.pyplot as plt


# parameters
# -----------------------------------------------------------
fileName = "/home/dsnl/pulse"
fileTag = ".h5"
file_r = fileName + fileTag
fs = 10000.0  		# sampling rate, [Hz]
pulse_amplitude = 2.0 # [nA]
pulse_duration = 150  # [ms] 
pulse_freq = 3.3      # [Hz]
total_duration = 5    # [min]
# -----------------------------------------------------------


# Generate pulse sequence from parameters
pulse_sequence = np.zeros(np.int(fs/pulse_freq))
pulse_duration_arr = 10 * pulse_duration
pulse_sequence[-pulse_duration_arr:] = pulse_amplitude * np.ones(pulse_duration_arr)
pulse_num = np.int((total_duration * 60) * pulse_freq)
pulse_total = np.tile(pulse_sequence, pulse_num)


# Create a new hdf5 file for injection
analogoutput = "-ao"
file_pulse = fileName + analogoutput + fileTag


# Write
f_w_pulse = h5py.File(file_pulse, 'w')
dset_pulse = f_w_pulse.create_dataset('analog-output', (np.size(pulse_total),), dtype='double', data=pulse_total)
f_w_pulse.close()

# plot
plt.plot(pulse_total)
plt.show()
