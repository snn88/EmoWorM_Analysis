import mne
import numpy

# select a random state
rs = numpy.random.RandomState(12345)

n_comp=10

#PIDS = range(1001, 1028)
PIDS = [1031, 1032]
BLOCKS = ['PV0', 'PV1', 'WM0', 'WM1']

picks = range(69)

# loop through the participants
for pid in PIDS:

    # loop through the blocks
    for block in BLOCKS:
   
        print pid, block
 
        # get the data file
        #dfile = "RAWDATA/%d_%s_raw.fif" % (pid, block)
        #dfile = "./FILTERDATA/%d_%s_1:30Hz_iir_raw.fif" % (pid, block)        
        dfile = "./FILTERDATA/%d_%s_0.1:30Hz-raw.fif" % (pid, block)

        # read data into mne
        raw = mne.io.read_raw_fif(dfile, preload=True, proj=False,
                                  add_eeg_ref=False)

        # build the ica
        #ica = mne.preprocessing.ICA(n_components=n_comp)
        ica = mne.preprocessing.ICA(random_state=rs)

        # fit the ica
        ica.fit(raw, picks=picks)

        # save the ica
        ica.save("./ICA/%d_%s-ica.fif" % (pid, block))
