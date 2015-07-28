import mne
import glob
import time
import matplotlib.pyplot as plt
import numpy as np

t0 = time.time()

#bdf_files = glob.glob("../ColorThresh/EEGDATA/*.bdf")
bdf_files = glob.glob("../ColorThresh/EEGDATA/103[12]_EmoWorM.bdf")

for bdf_file in bdf_files:

    print bdf_file
    # read the raw file
    raw = mne.io.read_raw_edf(bdf_file, preload=False, stim_channel='Status')
    # get stim channel data
    x1, t1 = raw[-1]
    x1 = x1[0]
    eve = mne.find_events(raw, mask=255, min_duration=0.1)
    print(eve)

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(111)
    ax1.plot(t1, x1, 'b')
    ax1.set_title('stim_channel="Status"')   
    ax1.set_xticks(np.arange(0, t1.max(), 100))
    ax1.set_ylim((0, 6e4))
    ax1.set_xlabel("Time (seconds)")
    xlim = ax1.get_xlim()
    ax1.plot(xlim, [4096, 4096], 'r-')
    ax1.plot(xlim, [8192, 8192], 'r-')
    ax1.plot(xlim, [16384, 16384], 'r-')
    ax1.plot(xlim, [32768, 32768], 'r-')
 
    fig.savefig(bdf_file[:-3]+"png")
    plt.close(fig)
    del(fig)

    print time.time() - t0
