import numpy as np
import mne
import matplotlib.pyplot as plt

picks = range(69)

raw_fname = "./RAWDATA/1001_PV0_raw.fif"

# read the raw data
raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                          add_eeg_ref=False)

# compute the ica
ica = mne.preprocessing.ICA()
ica.fit(raw, picks=picks)

# get the sources
src = ica.get_sources(raw)

# epoch the ica components
eve = mne.find_events(raw, mask=255)
epo = mne.Epochs(src, eve, [16384, 32768], -0.1, 1.5, preload=True,
                 proj=False, add_eeg_ref=False)
t = epo.times

X = epo.get_data()
Xbar = X.mean(0)
Xerr = X.std(0)

ylim = ((Xbar+Xerr).max(), (Xbar-Xerr).min())

fig = plt.figure()

for n in picks:

    ax = fig.add_subplot(10, 7, n+1)
    ax.plot(t, Xbar[n])
    ax.fill_between(t, Xbar[n]+Xerr[n], Xbar[n]-Xerr[n], alpha=0.5)
    ax.set_ylim(ylim)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title(n)

plt.show()
