import mne
import glob
import numpy as np

mne.set_log_level(False)

# generate a list of participant ids
PIDS = range(1001, 1021)
# remove participant 1018 (doesn't exist)
PIDS.pop(17)

# create an array to store epoch data
n_conditions = 4
n_times = 4097 # two seconds with sampling rate 2048
n_channels = 72
n_trials = 48
X = np.zeros((len(PIDS), n_conditions, n_trials, n_channels))

# loop through the participants
for p, pid in enumerate(PIDS):
#for p, pid in enumerate([1001]):

    # find the data files
    raw_fname_pv = glob.glob("./RAWDATA/%d_PV*.fif" % pid)
    raw_fname_wm = glob.glob("./RAWDATA/%d_WM*.fif" % pid)

    # read raw objects into mne
    raw_pv = mne.io.read_raw_fif(raw_fname_pv, preload=True, proj=False,
                                 add_eeg_ref=False)
    raw_wm = mne.io.read_raw_fif(raw_fname_wm, preload=True, proj=False,
                                 add_eeg_ref=False)

    # get the events
    eve_pv = mne.find_events(raw_pv, mask=255)
    eve_wm = mne.find_events(raw_wm, mask=255)

    # epoch the data
    epo_pv = mne.Epochs(raw_pv, eve_pv, [16384, 32768], -0.5, 1.5,
                        preload=True, #reject=dict(eeg=100e-6),
                        proj=False, add_eeg_ref=False)
    epo_wm = mne.Epochs(raw_wm, eve_wm, [16384, 32768], -0.5, 1.5,
                        preload=True, #reject=dict(eeg=100e-6),
                        proj=False, add_eeg_ref=False)
    x_pv_neu = epo_pv['16384'].get_data()
    x_pv_neg = epo_pv['32768'].get_data()
    x_wm_neu = epo_wm['16384'].get_data()
    x_wm_neg = epo_wm['32768'].get_data()
    for i in range(n_trials):
        for j in range(n_channels):
            X[p, 0, i, j] = x_pv_neu[i, j].max() - x_pv_neu[i, j].min()
            X[p, 1, i, j] = x_pv_neg[i, j].max() - x_pv_neu[i, j].min()
            X[p, 2, i, j] = x_wm_neu[i, j].max() - x_pv_neu[i, j].min()
            X[p, 3, i, j] = x_wm_neg[i, j].max() - x_pv_neu[i, j].min()

    '''
    # compute the evoked data
    evo_pv_neu = epo_pv['16384'].average(picks=range(64))
    evo_pv_neg = epo_pv['32768'].average(picks=range(64))
    evo_wm_neu = epo_wm['16384'].average(picks=range(64))
    evo_wm_neg = epo_wm['32768'].average(picks=range(64))

    # store data in array
    X[p, 0] = evo_pv_neu.data
    X[p, 1] = evo_pv_neg.data
    X[p, 2] = evo_wm_neu.data
    X[p, 3] = evo_wm_neg.data
    '''
