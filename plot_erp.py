import mne
import glob
import numpy as np
import matplotlib.pyplot as plt

mne.set_log_level(False)

# generate a list of participant ids
PIDS = range(1001, 1022)

# use only the first 64 channels
picks = range(64)

# plot the data
lout = mne.channels.read_layout('biosemi64.lout', path='.')

# loop through the participants
for pid in PIDS:

    # find the data files
    # raw_fname = glob.glob("./RAWDATA/%d*.fif" % pid)
    # raw_fname = glob.glob("./FILTERDATA/%d*.fif" % pid)
    raw_fname = glob.glob("./POSTICA/%d*.fif" % pid)    

    # read raw objects into mne
    raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                              add_eeg_ref=False)

    # get the events
    eve = mne.find_events(raw, mask=255)

    # epoch the data
    epo = mne.Epochs(raw, eve, [16384, 32768], -0.1, 0.5,
                     preload=True, reject=dict(eeg=1e-3),
                     proj=False, add_eeg_ref=False, picks=picks)
    print pid, epo._data.shape[0]

    # get the evoked data
    evo = epo.average() 
    err = epo.standard_error()
    t = epo.times   
 
    vmin, vmax = (evo.data - err.data).min(), (evo.data + err.data).max()

    fig = plt.figure(figsize=(20, 10))
    for n in range(64):

        V = evo.data[n]

        ax = fig.add_axes(lout.pos[n])
        ax.plot(t, V)
        ax.fill_between(t, V+err.data[n], V-err.data[n],  facecolor='blue', alpha=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(vmin, vmax)

    fig.savefig('%d_erp.png' % pid)
    plt.close(fig)

plt.show()
