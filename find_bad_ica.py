import matplotlib.pyplot as plt
import mne
import numpy as np

mne.set_log_level(False)

#PIDS = range(1001, 1030)
PIDS = [1031, 1032]
BLOCKS = ['PV0', 'PV1', 'WM0', 'WM1']

kurt = 58
skew = 5.3
var=None
pear=0.23

# loop through the participants
for pid in PIDS:

    # loop through the blocks
    for block in BLOCKS:
    
        # get the data files
        raw_file = "./FILTERDATA/%d_%s_0.1:30Hz-raw.fif" % (pid, block)        
        ica_file = "./ICA/%d_%s-ica.fif" % (pid, block)

        # read data into mne
        raw = mne.io.read_raw_fif(raw_file, preload=True, proj=False,
                                  add_eeg_ref=False)
        ica = mne.preprocessing.read_ica(ica_file)

        # compute the blink channel
        ix, = np.where(np.in1d(raw.ch_names, ['Fpz', 'Fp1', 'Fp2']))
        blink = raw[ix][0].mean(0)

        # detect artifacts
        ica.detect_artifacts(raw, eog_ch=blink, eog_criterion=pear,
                             kurt_criterion=kurt, skew_criterion=skew,
                             var_criterion=var)

        # reconstitute raw
        print pid, ica.exclude
        raw = ica.apply(raw, exclude=ica.exclude)
        raw.save('./POSTICA/%d_%s_postica-raw.fif' % (pid, block),
                 overwrite=True)
