import os
import mne
import numpy as np
import matplotlib.pyplot as plt

# load a sample epoch file
epo = mne.read_epochs('./EPO/1001_PV0-epo.fif', proj=False, add_eeg_ref=False)
epo.info['picks'] = None
epo.pick_channels(epo.ch_names[:64])

t = epo.times

# load the layout file
lout = mne.channels.read_layout('biosemi.lay')

# load the erp data
erp = np.load('evo-all.npy')

