import matplotlib.pyplot as plt
import mne
import numpy as np

n_pca = 10
scale = 1e-5
ica_scale = 10
n_channels = 64

PIDS = range(1001, 1022)
BLOCKS = ['PV0', 'PV1', 'WM0', 'WM1']

# loop through the participants
for pid in PIDS:

    # loop through the blocks
    for block in BLOCKS:
    
        # get the data file
        # dfile = "RAWDATA/%d_%s_raw.fif" % (pid, block)
        dfile = "./FILTERDATA/%d_%s_1:30Hz_1s_raw.fif" % (pid, block)        

        # read data into mne
        raw = mne.io.read_raw_fif(dfile, preload=True, proj=False,
                                  add_eeg_ref=False)

        # read the ica
        ica = mne.preprocessing.read_ica("ICA/%d_%s_ica.fif" % (pid, block))

        # epoch the data

        # find the events
        eve = mne.find_events(raw, mask=255)

        # epoch the data
        epo = mne.Epochs(raw, eve, [16384, 32768], -0.5, 1.5,
                         preload=True, proj=False, add_eeg_ref=False)

        X = epo.get_data()
        t = epo.times

        # get the ica sources
        src = ica.get_sources(epo)
        Y = src.get_data()

        # loop through the trials
        for trial in range(48):

            x = X[trial, :n_channels]
            y = Y[trial]

            # open a new figure
            fig, ax = plt.subplots(2, figsize=(40, 20))

            # plot each channel
            for n in range(n_channels):
                # apply a dc offset
                ax[0].plot(t, x[n]-n*scale)

            # plot each component
            for n in range(n_pca):
                y[n] -= y[n, 0]
                ax[1].plot(t, y[n]-n*ica_scale)
            
            ax[0].set_xlim((t[0], t[-1]))
            ax[1].set_xlim((t[0], t[-1]))

            ax[0].set_yticks(np.arange(0, -n_channels, -1)*scale)
            ax[0].set_yticklabels(epo.ch_names[:n_channels])

            ax[1].set_yticks(np.arange(0, -n_pca, -1)*ica_scale)

            figname = "%d_%s_%d_epo-ica.png" % (pid, block, trial)
            fig.savefig(figname)

            plt.close(fig)
