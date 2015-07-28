import matplotlib.pyplot as plt
import mne
import numpy as np


# define the data file
raw_fname = './RAWDATA/1001_PV0_raw.fif'

# get the index to a "bad" channel
n = 2

# read the raw data
raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                          add_eeg_ref=False)
raw = raw.crop(tmax=10)

# pic out some data
x1 = raw[n][0][0]

# filter the data
x2 = mne.filter.band_pass_filter(x1, raw.info['sfreq'], 1, 30, '1s')

# open a figure
fig = plt.figure()
ax = fig.add_subplot(111)

# start both signals at zero
x1 -= x1[0]
x2 -= x2[0]

# plot the data
ax.plot(x1)
ax.plot(x2)
ax.set_yticks([])
ax.set_xticks([])

plt.show()
