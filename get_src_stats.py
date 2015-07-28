import numpy as np
import mne
from os import path
from scipy import stats

# identify the participants
pids = range(1001, 1030)

# identify the conditions
blocks = ['PV0', 'PV1', 'WM0', 'WM1']

# initialize some empty lists
K = []  # kurtosis
S = []  # skew
P = []  # pearsons (eog)
V = []  # variance

# loop through the participants
for pid in pids:

    # loop through the blocks
    for block in blocks:
       
        # get the filenames
        raw_fname = './FILTERDATA/%d_%s_0.1:30Hz-raw.fif' % (pid, block)
        ica_fname = './ICA/%d_%s-ica.fif' % (pid, block) 

        # make sure that the filenames exist
        assert path.exists(raw_fname) and path.exists(ica_fname)

        # read the data files
        raw = mne.io.read_raw_fif(raw_fname, proj=False, add_eeg_ref=False,
                                  preload=True)
        ica = mne.preprocessing.read_ica(ica_fname)

        # compute the 'blink channel'
        ix, = np.where(np.in1d(raw.ch_names, ['Fpz', 'Fp1', 'Fp2'])) 
        blink = raw[ix][0].mean(0)

        # compute the ica sources
        src = ica.get_sources(raw)

        # score the sources
        k = mne.preprocessing.ica._find_sources(src._data, None, 
                                                stats.kurtosis)
        s = mne.preprocessing.ica._find_sources(src._data, None, 
                                                stats.skew)
        p = mne.preprocessing.ica._find_sources(src._data, blink, 
                                                'pearsonr')
        v = mne.preprocessing.ica._find_sources(src._data, None, 
                                                np.var)

        # update the lists
        K.append(k), S.append(s), P.append(p), V.append(v)

        print pid, block

# convert lists to arrays
K = np.array(K)
S = np.array(S)
P = np.array(P)
V = np.array(V)

# save the output
np.savetxt('kurt.txt', K)
np.savetxt('skew.txt', S)
np.savetxt('var.txt', V)
np.savetxt('eog.txt', P)

# flatten, sort, absolute value
k = abs(K.flatten())
s = abs(S.flatten())
p = abs(P.flatten())
v = abs(V.flatten())
k.sort()
s.sort()
p.sort()
v.sort()

# get the 95th percentile
i95 = int(.95*len(k))
k95 = k[i95]
s95 = s[i95]
p95 = p[i95]
v95 = v[i95]
