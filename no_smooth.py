import mne

# define the epoch file
epo_fname = "./EPO/1001_PV0-epo.fif"

# read the epoch file into python
epo = mne.read_epochs(epo_fname, proj=False, add_eeg_ref=False)

# read the layout file
lout = mne.channels.read_layout('biosemi.lay')

# plot the image epochs
# mne.viz.plot_topo_image_epochs(epo, lout, vmin=epo._data.min()*1e6,
#                               vmax=epo._data.max()*1e6, sigma=0)

mne.viz.plot_image_epochs(epo, picks=[35], vmin=-200, vmax=200)
