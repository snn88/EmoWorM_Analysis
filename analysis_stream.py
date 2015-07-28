import numpy as np
import mne
from os import path
import time
import glob
import matplotlib.pyplot as plt

# script start time
t0 = time.time()

mne.set_log_level(False)

pids = range(1001, 1025)  # list of participant ids
blocks = ['PV0', 'PV1', 'WM0', 'WM1']  # the block types

l_freq=0.1  # highpass frequency
h_freq=30  # lowpass frequency
picks = range(69)  # electrodes to use

tmin = -0.1  # epoch start time
tmax = 1.0  # epoch end time
rej = 1e-3  # rejection criteria (in volts)

# read the biosemi layout
lout = mne.channels.read_layout('biosemi.lay')

# set some parameters
n_p = len(pids)  # number of participants
n_ch = len(picks)  # number of channels
n_t = 2254  # number of time points

# create an array to store data
X = np.zeros((n_p, 4, 64, n_t))

# loop through the participants
for p, pid in enumerate(pids):
    # loop through the blocks
    for b, block in enumerate(blocks):

        # get the raw data
        raw_fname = "./RAWDATA/%d_%s_raw.fif" % (pid, block)

        #####################################
        ### STEP 1: Re-reference the data ###
        #####################################

        # read the raw data
        raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                                  add_eeg_ref=False)
        # re-reference the data
        # reref_ix = raw.ch_names.index('Cz')
        reref_ix = np.in1d(raw.ch_names, ['M1', 'M2'])
        raw._data[picks] -= raw._data[reref_ix].mean(0)

        ###############################
        ### STEP 2: Filter the data ###
        ###############################

        # filter the data
        raw.filter(l_freq=l_freq, h_freq=h_freq, l_trans_bandwidth=0.09)

        ###########################
        ### STEP 3: Perform ICA ###
        ###########################

        # get the "eog signal"
        ix, = np.where(np.in1d(raw.ch_names, ['Fpz', 'Fp1', 'Fp2']))
        blink = raw[ix][0].mean(0)

        # perform ica
        ica = mne.preprocessing.ICA()
        ica.fit(raw, picks=picks)
 
        # look for artifacts
        ica.detect_artifacts(raw, eog_ch=blink, eog_criterion=0.5)
       
        # re-compose the data
        raw = ica.apply(raw, exclude=ica.exclude)

        # save the data
        raw.save('./POSTICA/%d_%s_postica-raw.fif' % (pid, block), overwrite=True)
        
        t = time.time()
        print pid, block, t-t0
        t0 = t

    # read the raw files per condition
    raw_pv = glob.glob('./POSTICA/%d_PV*.fif' % (pid))
    raw_wm = glob.glob('./POSTICA/%d_WM*.fif' % (pid))

    # read the raw data into python
    raw_pv = mne.io.read_raw_fif(raw_pv, preload=True, proj=False,
                                 add_eeg_ref=False)
    raw_wm = mne.io.read_raw_fif(raw_wm, preload=True, proj=False,
                                 add_eeg_ref=False)


    # get the events
    eve_pv = mne.find_events(raw_pv, mask=255)
    eve_wm = mne.find_events(raw_wm, mask=255)

    # epoch the data
    epo_pv = mne.Epochs(raw_pv, eve_pv, [16384, 32768], tmin, tmax,
                        preload=True, reject=dict(eeg=rej),
                        proj=False, add_eeg_ref=False, picks=range(64))
    epo_wm = mne.Epochs(raw_wm, eve_wm, [16384, 32768], tmin, tmax,
                        preload=True, reject=dict(eeg=rej),
                        proj=False, add_eeg_ref=False, picks=range(64))

    # print the number of trials
    print pid, epo_pv['16384'].get_data().shape[0], \
               epo_pv['32768'].get_data().shape[0], \
               epo_wm['16384'].get_data().shape[0], \
               epo_wm['32768'].get_data().shape[0]

    # get the evoked data
    evo_pv_neu = epo_pv['16384'].average()
    evo_pv_neg = epo_pv['32768'].average()
    evo_wm_neu = epo_wm['16384'].average()
    evo_wm_neg = epo_wm['32768'].average()
 
    # store data
    X[p, 0] = evo_pv_neu.data
    X[p, 1] = evo_pv_neg.data
    X[p, 2] = evo_wm_neu.data
    X[p, 3] = evo_wm_neg.data

# get the times
t = epo_pv.times

# open a figure for the fmap
fig1 = plt.figure()

# open a figure for the erps
fig2 = plt.figure()
ylim = (X.mean(0).min(), X.mean(0).max())

# perform a 2 way, within subjects, repeated measures ANOVA
f, p = mne.stats.f_mway_rm(X, [2, 2])
# find the maximum f-value
fmax = f.max()

# perform fdr correction
sig_fdr, p_fdr = mne.stats.fdr_correction(p)
fmin_fdr = f[sig_fdr].min()

# perform bonferroni correction
p_bonf = p*n_ch*n_t
sig_bonf = p_bonf < 0.05
fmin_bonf = f[sig_bonf].min()

# loop through the eeg channels
for n in range(64):

    # get the f-values
    f, p = mne.stats.f_mway_rm(X[:, :, n], [2, 2])
    # open a new axis for f plots
    ax = fig1.add_axes(lout.pos[n])

    # plot the f-values
    ax.plot(t, f.T)
    # plot the fdr cutoff
    ax.plot([t[0], t[-1]], [fmin_fdr, fmin_fdr], 'k--')
    # plot the bonferonni cutoff
    ax.plot([t[0], t[-1]], [fmin_bonf, fmin_bonf], 'k--')
    ax.set_ylim((0, fmax))
    ax.set_xlim((t[0], t[-1]))

    # open an axis for erp plots
    ax = fig2.add_axes(lout.pos[n])
    ax.plot(t, X[:, 0, n].mean(0), 'c')  # neutral passive view
    ax.plot(t, X[:, 1, n].mean(0), 'm')  # negative passive view
    ax.plot(t, X[:, 2, n].mean(0), 'b')  # neutral working memory
    ax.plot(t, X[:, 3, n].mean(0), 'r')  # negative working memory
    ax.set_ylim(ylim)
    ax.set_xlim((t[0], t[-1]))
    ax.plot([0, 0], ylim, 'k--')
    ax.set_yticks([])

# show the two plots
plt.show()
