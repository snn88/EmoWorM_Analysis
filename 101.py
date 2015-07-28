import mne
import glob
import matplotlib.pyplot as plt

pid = 1001
conditions = ['PV0', 'WM0', 'PV1', 'WM1']
picks = range(64)

# get the raw data files
raw_fnames = glob.glob('./RAWDATA/%d*.fif' % pid)

# read the raw data
raw = mne.io.read_raw_fif(raw_fnames, preload=True, proj=False,
                          add_eeg_ref=False)

# re-reference to mastoids
# raw._data -= raw._data[66:68].mean(0)
# re-reference to average
raw._data -= raw._data[:64].mean(0)

# get the events
eve = mne.find_events(raw, mask=255)
# epoch the data
epo = mne.Epochs(raw, eve, [16384, 32768], -0.1, 1.0,
                 preload=True, proj=False, picks=picks)

# get the evoked ata
evo_neu = epo['16384'].average()
evo_neg = epo['32768'].average()

lout = mne.channels.read_layout('biosemi.lay')

mne.viz.plot_topo([evo_neu, evo_neg], layout=lout, color=['b', 'r'])

plt.show()
