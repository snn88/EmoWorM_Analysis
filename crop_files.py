import glob
import mne
import numpy as np

mne.set_log_level(False)

# bdf directory
bdf_dir = "../ColorThresh/EEGDATA/"

# read the break file
breaks = np.genfromtxt("./bdf_breaks.txt", delimiter=",")

# list of participant IDs
#participants = range(1001, 1021)
participants = [1031, 1032]

# loop through the participants
for pid in participants:

    # get the breaks for this participant
    brk, = breaks[breaks[:, 0] == pid, :]

    # find the .bdf file
    bdf_file = glob.glob(bdf_dir + "%d_EmoWorM.bdf" % pid)[0]
    #print bdf_file

    # read the bdf file into mne
    raw = mne.io.read_raw_edf(bdf_file, stim_channel="Status", preload=True)

    # set counters for each block type
    pv_counter = 0
    wm_counter = 0

    # loop through the crop
    for b in range(2, 6):
        
        # crop the file
        this_raw = raw.crop(tmin=brk[b-1], tmax=brk[b], copy=True)
        eve = mne.find_events(this_raw, mask=255)

        # allow 48 (passive view) or 144 (working memory) events only
        assert np.in1d(len(eve), [48, 144]).all()

        # construct the eeg filename
        if len(eve) == 48:
            # passive view
            fname = "./RAWDATA/%d_PV%d-raw.fif" % (pid, pv_counter)
            pv_counter += 1
        elif len(eve) == 144:
            # working memory
            fname = "./RAWDATA/%d_WM%d-raw.fif" % (pid, wm_counter)
            wm_counter += 1

        # save the data
        this_raw.save(fname, proj=False)
