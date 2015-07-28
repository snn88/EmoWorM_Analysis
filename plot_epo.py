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

file_path = './EPO/%d_%s-epo.fif'
blocks = ['PV0', 'PV1', 'WM0', 'WM1']

# loop through the participants
for p, pid in enumerate(pids):
    for b, block in enumerate(blocks):

        # read the epoch data
        raw_fname = file_path % (pid, block)
        epo = mne.read_epochs(raw_fname, proj=False,
                              add_eeg_ref=False)
        epo.picks = None
        epo.pick_channels(epo.ch_names[:64])      
 
        epo_neu = epo['16384']
        epo_neg = epo['32768']

        rng_neu = epo_neu._data.max(2) - epo_neu._data.min(2)
        rng_neg = epo_neg._data.max(2) - epo_neg._data.min(2)
        rej_neu = rng_neu > rej
        rej_neg = rng_neg > rej

        evo_neu = epo_neu.average()
        evo_neg = epo_neg.average()
        err_neu = epo_neu.standard_error()
        err_neg = epo_neg.standard_error()
        t = epo.times
        ylim = (-1e-4, 1e-4)

        # plot the epoch data
        fig = plt.figure(figsize=(20, 10))
        for n in range(64):
            ax = fig.add_axes(lout.pos[n])
            if block < 2:
                cneu = 'c'
                cneg = 'm'
            else:
                cneu = 'b'
                cneg = 'r'
            x1 = evo_neu.data[n]
            e1 = err_neu.data[n]
            x2 = evo_neg.data[n]
            e2 = err_neg.data[n]
            ax.plot(t, x1, cneu)
            ax.plot(t, x2, cneg)
            ax.fill_between(t, x1-e1, x1+e1, color=cneu, alpha=0.5)
            ax.fill_between(t, x2-e2, x2+e2, color=cneg, alpha=0.5)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_ylim(ylim)
            ax.set_xlim((t[0], t[-1]))
            ax.set_title('Neu: %d, Neg: %d' % (rej_neu[:, n].sum(),
                                               rej_neg[:, n].sum())) 

        fig.savefig('./EPO/%d_%s-evo.png' % (pid, block))
        plt.close(fig)

plt.show()
