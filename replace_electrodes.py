import mne

bads = [
        #[1015, 'WM1', 'F6', 'EXG6'],
        #[1015, 'PV1', 'F6', 'EXG6'],
        #[1018, 'PV0', 'F6', 'EXG8'],
        #[1018, 'WM0', 'F6', 'EXG8'],
        #[1018, 'PV1', 'F6', 'EXG8'],
        #[1018, 'WM1', 'F6', 'EXG8'],
        #[1021, 'WM1', 'F6', 'EXG8'],
        #[1021, 'PV1', 'F6', 'EXG8'],
        #[1022, 'PV0', 'F6', 'EXG8'],
        #[1022, 'WM0', 'F6', 'EXG8'],
        #[1022, 'PV1', 'F6', 'EXG8'],
        #[1022, 'WM1', 'F6', 'EXG8'],
        #[1025, 'PV0', 'F6', 'EXG8'],
        #[1025, 'WM0', 'F6', 'EXG8'],
        #[1025, 'PV1', 'F6', 'EXG8'],
        #[1025, 'WM1', 'F6', 'EXG8'],
        #[1026, 'PV0', 'F6', 'EXG8'],
        #[1026, 'WM0', 'F6', 'EXG8'],
        #[1026, 'PV1', 'F6', 'EXG8'],
        #[1026, 'WM1', 'F6', 'EXG8'],
        #[1027, 'PV0', 'F6', 'EXG8'],
        #[1027, 'WM0', 'F6', 'EXG8'],
        #[1027, 'PV1', 'F6', 'EXG8'],
        #[1027, 'WM1', 'F6', 'EXG8'],
        #[1028, 'PV0', 'F6', 'EXG8'],
        #[1028, 'WM0', 'F6', 'EXG8'],
        #[1028, 'PV1', 'F6', 'EXG8'],
        #[1028, 'WM1', 'F6', 'EXG8'],
        #[1029, 'PV0', 'F6', 'EXG8'],
        #[1029, 'WM0', 'F6', 'EXG8'],
        #[1029, 'PV1', 'F6', 'EXG8'],
        #[1029, 'WM1', 'F6', 'EXG8'],
        #[1030, 'PV0', 'F6', 'EXG8'],
        #[1030, 'WM0', 'F6', 'EXG8'],
        #[1030, 'PV1', 'F6', 'EXG8'],
        #[1030, 'WM1', 'F6', 'EXG8'],
        [1031, 'PV0', 'F6', 'EXG8'],
        [1031, 'WM0', 'F6', 'EXG8'],
        [1031, 'PV1', 'F6', 'EXG8'],
        [1031, 'WM1', 'F6', 'EXG8'],
        [1032, 'PV0', 'F6', 'EXG8'],
        [1032, 'WM0', 'F6', 'EXG8'],
        [1032, 'PV1', 'F6', 'EXG8'],
        [1032, 'WM1', 'F6', 'EXG8']]

for b in bads:
    pid, block, bad_ch, new_ch = b
    
    # read the raw file
    raw_fname = './RAWDATA/%d_%s-raw.fif' % (pid, block)
    raw = mne.io.read_raw_fif(raw_fname, preload=True,
                              proj=False, add_eeg_ref=False)

    # replace bad electrode
    bad_ix = raw.ch_names.index(bad_ch)
    new_ix = raw.ch_names.index(new_ch)

    raw._data[bad_ix] = raw._data[new_ix]

    # save the data
    raw.save(raw_fname, overwrite=True)
