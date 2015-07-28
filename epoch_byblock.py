import mne
import glob
import numpy as np
import matplotlib.pyplot as plt

mne.set_log_level(False)

#pids = range(1001, 1030)
pids = [1031, 1032]
n_p = len(pids)
picks = range(69)
n_ch = len(picks)
n_t = 2254

lout = mne.channels.read_layout('biosemi.lay')

file_path = './POSTICA/%d_%s_postica-raw.fif'
blocks = ['PV0', 'PV1', 'WM0', 'WM1']

# loop through the participants
for p, pid in enumerate(pids):
    for b, block in enumerate(blocks):

        # read the raw data
        raw_fname = file_path % (pid, block)
        
        raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                                  add_eeg_ref=False)
        
        # get the events
        eve = mne.find_events(raw, mask=255)

        # epoch the data
        epo = mne.Epochs(raw, eve, [16384, 32768], -0.1, 1.0,
                         preload=True, #reject=dict(eeg=1e-3),
                         proj=False, add_eeg_ref=False, picks=picks)

        # save the epoch data
        epo.save('./EPO/%d_%s-epo.fif' % (pid, block))
        print pid, block
