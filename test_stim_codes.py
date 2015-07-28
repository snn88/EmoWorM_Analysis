import mne

bdf_file = "../ColorThresh/EEGDATA/1001_EmoWorM.bdf"

raw = mne.io.read_raw_edf(bdf_file, stim_channel="Status")

eve = mne.find_events(raw, mask=-256)
