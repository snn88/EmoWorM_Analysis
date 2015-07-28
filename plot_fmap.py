import mne
import glob
import numpy as np
import matplotlib.pyplot as plt

mne.set_log_level(False)

pids = range(1001, 1033)
n_p = len(pids)
picks = range(64)
n_ch = len(picks)
n_t = 2254
rej = 1e-3

lout = mne.channels.read_layout('biosemi.lay')

X = np.zeros((n_p, 4, n_ch, n_t))

# loop through the participants
for p, pid in enumerate(pids):

    # read the epoch data
    epo_pv = mne.read_epochs('./EPO/%d_PV-epo.fif' % pid, proj=False,
                             add_eeg_ref=False)
    epo_wm = mne.read_epochs('./EPO/%d_WM-epo.fif' % pid, proj=False,
                             add_eeg_ref=False)

    # exclude F6 for two participants
    if pid in [1021, 1024]:
        epo_pv._data[:, 40] = np.zeros((96, n_t))
        epo_wm._data[:, 40] = np.zeros((96, n_t))

    # re-reference the channels
    # average ref
    ref_pv = epo_pv._data[:, :64].mean(1)
    ref_wm = epo_wm._data[:, :64].mean(1)
    '''
    # mastoid ref
    ref_pv = epo_pv._data[:, (66, 67)].mean(1)
    ref_wm = epo_wm._data[:, (66, 67)].mean(1)
    '''

    for n in range(64):
        epo_pv._data[:, n] -= ref_pv
        epo_wm._data[:, n] -= ref_wm

    # drop bad epochs
    bad_pv, = np.where(((epo_pv._data.max(2) - epo_pv._data.min(2)) > rej).any(1))
    bad_wm, = np.where(((epo_wm._data.max(2) - epo_wm._data.min(2)) > rej).any(1))
    bad_pv = bad_pv[bad_pv < 64]
    bad_wm = bad_wm[bad_wm < 64]

    epo_pv.drop_epochs(bad_pv)
    epo_wm.drop_epochs(bad_wm)
    
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
    X[p, 0] = evo_pv_neu.data[:64]
    X[p, 1] = evo_pv_neg.data[:64]
    X[p, 2] = evo_wm_neu.data[:64]
    X[p, 3] = evo_wm_neg.data[:64]

t = epo_pv.times
fig1 = plt.figure()
fig2 = plt.figure()
ylim = (X.mean(0).min(), X.mean(0).max())

f, p = mne.stats.f_mway_rm(X, [2, 2])
fmax = f.max()

# fdr correction
sig_fdr, p_fdr = mne.stats.fdr_correction(p)
if sig_fdr.sum() > 0:
    fmin_fdr = f[sig_fdr].min()
else:
    fmin_fdr = fmax

# bonferroni correction
p_bonf = p*n_ch*n_t
sig_bonf = p_bonf < 0.05
if sig_bonf.sum() > 0:
    fmin_bonf = f[sig_bonf].min()
else:
    fmin_bonf = fmax

for n in range(64):

    f, p = mne.stats.f_mway_rm(X[:, :, n], [2, 2])
    ax = fig1.add_axes(lout.pos[n])
    
    ax.plot(t, f.T)
    ax.plot([0, 0], [0, fmax], 'k--')
    ax.plot([t[0], t[-1]], [fmin_fdr, fmin_fdr], 'k--')
    ax.plot([t[0], t[-1]], [fmin_bonf, fmin_bonf], 'k--')
    ax.set_ylim((0, fmax))
    ax.set_xlim((t[0], t[-1]))
    ax.set_title(evo_pv_neu.ch_names[n])
    
    ax = fig2.add_axes(lout.pos[n])
    ax.plot(t, X[:, 0, n].mean(0), 'c')
    ax.plot(t, X[:, 1, n].mean(0), 'm')
    ax.plot(t, X[:, 2, n].mean(0), 'b')
    ax.plot(t, X[:, 3, n].mean(0), 'r')
    ax.set_ylim(ylim)
    ax.set_xlim((t[0], t[-1]))
    ax.plot([0, 0], ylim, 'k--')
    ax.set_yticks([])
    ax.set_title(evo_pv_neu.ch_names[n])
    
plt.show() 

