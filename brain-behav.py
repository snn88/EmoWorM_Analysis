import os
import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# load a sample epoch file
epo = mne.read_epochs('./EPO/1001_PV0-epo.fif', proj=False, add_eeg_ref=False)
epo.info['picks'] = None
epo.pick_channels(epo.ch_names[:64])

t = epo.times*1e3

# load the layout file
lout = mne.channels.read_layout('biosemi.lay')

# load the erp data
erp = np.load('evo-all.npy')
erp *= 1e6

# read the scores
scores = np.genfromtxt('scores.txt')
x1 = (scores[:, 0] - scores[:, 1]) / scores[:, 0]

r, p = np.zeros((64, 2254)), np.zeros((64, 2254))
for n in range(64):
    for m in range(2254):
        # wm neg - pv neg
        x2 = erp[:, 3, n, m] - erp[:, 1, n, m]
        r[n, m], p[n, m] = stats.pearsonr(x1, x2) 


fig = plt.figure()
for n in range(64):
    ax = fig.add_axes(lout.pos[n])
    ax.plot(t, -np.log(p[n]))
    ax.set_ylim((-np.log(0.05), -np.log(p.min())))
    ax.set_xlim((t[0], t[-1]))

plt.show()
