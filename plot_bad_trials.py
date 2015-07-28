import mne
import glob
import numpy as np
import matplotlib.pyplot as plt

mne.set_log_level(False)

pids = range(1001, 1022)
n_p = len(pids)
picks = range(64)
n_ch = len(picks)
n_t = 1230
thresh = 5e-5

lout = mne.channels.read_layout('biosemi.lay')

# loop through the participants
for p, pid in enumerate(pids):

    # read the raw data
    raw_pv = glob.glob('./POSTICA/%d_PV*.fif' % pid)
    raw_wm = glob.glob('./POSTICA/%d_WM*.fif' % pid)

    raw_pv = mne.io.read_raw_fif(raw_pv, preload=True, proj=False,
                                 add_eeg_ref=False)
    raw_wm = mne.io.read_raw_fif(raw_wm, preload=True, proj=False,
                                 add_eeg_ref=False)

    # get the events
    eve_pv = mne.find_events(raw_pv, mask=255)
    eve_wm = mne.find_events(raw_wm, mask=255)

    # epoch the data
    epo_pv = mne.Epochs(raw_pv, eve_pv, [16384, 32768], -0.1, 0.5,
                        preload=True, #reject=dict(eeg=1e-4),
                        proj=False, add_eeg_ref=False, picks=picks)
    epo_wm = mne.Epochs(raw_wm, eve_wm, [16384, 32768], -0.1, 0.5,
                        preload=True, #reject=dict(eeg=1e-4),
                        proj=False, add_eeg_ref=False, picks=picks)
    pv_neu = epo_pv['16384'].get_data()
    pv_neg = epo_pv['32768'].get_data()
    wm_neu = epo_wm['16384'].get_data()
    wm_neg = epo_wm['32768'].get_data()   

    # plot the channels 
    fig = plt.figure(figsize=(20, 10))
    for ch in picks:
        x = lout.pos[ch, 0]
        y = lout.pos[ch, 1]
        n1 = ((pv_neu[:, ch].max(1) - pv_neu[:, ch].min(1)) > thresh).sum()
        n2 = ((pv_neg[:, ch].max(1) - pv_neg[:, ch].min(1)) > thresh).sum()
        n3 = ((wm_neu[:, ch].max(1) - wm_neu[:, ch].min(1)) > thresh).sum() 
        n4 = ((wm_neg[:, ch].max(1) - wm_neg[:, ch].min(1)) > thresh).sum()

        fig.text(x, y, n1, color='c')
        fig.text(x+.02, y, n2, color='m')
        fig.text(x, y+.02, n3, color='b')
        fig.text(x+.02, y+.02, n4, color='r')

    fig.savefig('%d_bads.png' % pid)
    plt.close(fig)

plt.show()
