import glob
import mne

# set low and high frequencies
l_freq = 0.1
h_freq = 30

# get all the raw data files
raw_files = glob.glob('./RAWDATA/103[12]*-raw.fif')

# loop through the files
for raw_fname in raw_files:

    print raw_fname
    # read data into mne
    raw = mne.io.read_raw_fif(raw_fname, preload=True, proj=False,
                              add_eeg_ref=False)

    raw.filter(l_freq=l_freq, h_freq=h_freq, l_trans_bandwidth=0.09)
    new_fname = raw_fname.replace('-raw.fif', '_%s:%sHz-raw.fif' % \
                                  (l_freq, h_freq))
    new_fname = new_fname.replace('./RAWDATA', './FILTERDATA')
    raw.save(new_fname, overwrite=True)
