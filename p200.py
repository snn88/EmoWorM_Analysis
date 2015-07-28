import os
import mne
import numpy as np
import matplotlib.pyplot as plt

# load a sample epoch file
epo = mne.read_epochs('./EPO/1001_PV0-epo.fif', proj=False, add_eeg_ref=False)
epo.info['picks'] = None
epo.pick_channels(epo.ch_names[:64])

t = epo.times*1e3

# load the layout file
lout = mne.channels.read_layout('biosemi.lay')

# load the erp data
erp = np.load('evo-all.npy')
erp *= 1e6

# get the time indices
tix = np.logical_and(t > 150, t < 210)

# get the channel indices
ch = ['C1', 'Cz', 'C2', 'CP1', 'CPz', 'CP2', 'P1', 'Pz', 'P2']
chix = np.in1d(epo.ch_names, ch)

# plot the erp
x = erp[:,:,chix].mean(-2).mean(0)

# open a new figure
fig, ax = plt.subplots()

# loop through the conditions
for i, c in enumerate(['c', 'm', 'b', 'r']):

    ax.plot(t, x[i], c)

#ax.plot(t[sig[0]], 9e-6*np.ones(sig[0].sum()), 'k*')
ax.set_xlim((t[0], t[-1]))
ylim = ax.get_ylim()
ax.fill_between(t, ylim[0], ylim[1], where=tix,
                color='k', alpha=0.3)
ax.plot((0, 0), ylim, 'k--')
ax.set_ylim(ylim)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Potential (uV)')
# plot the topo map
fig, ax = plt.subplots()
for n in range(64):
    mfc='w'
    if epo.ch_names[n] in ch:
        mfc='g'
    ax.plot(lout.pos[n, 0], lout.pos[n, 1], mec='k', marker='o', ls='None',
            ms=30, mfc=mfc)
    ax.text(lout.pos[n, 0], lout.pos[n, 1], epo.ch_names[n],
    ha='center', va='center') 

ax.set_aspect(1)
ax.set_frame_on(False)
ax.set_xticks([])
ax.set_yticks([])

# plot the f maps
f, p = mne.stats.f_mway_rm(erp[:, :, :, tix].mean(3), [2, 2])
fig = plt.figure()
vmax = abs(erp[:, :, :, tix].mean(-1).mean(0)).max()
vmin = -vmax
titles = ['Passive View\nNeutral', 'Passive View\nNegative',
          'Working Memory\nNeutral', 'Working Memory\nNegative']
for n in range(4):
    ax = fig.add_subplot(2, 4, n+1)
    x = erp[:, n, :, tix].mean(0).mean(0)    
    mne.viz.plot_topomap(x, lout.pos, axis=ax, vmin=vmin, vmax=vmax)
    ax.set_title(titles[n])

titles = ['Task', 'Valence', 'Valence x Task']
for n in range(3):
    ax = fig.add_subplot(2, 3, n+4)
    mne.viz.plot_topomap(f[n], lout.pos, axis=ax, vmin=0, vmax=f.max(),
                         cmap=plt.cm.Reds)
    ax.set_title(titles[n])
plt.show()
