import mne
from os import path
import matplotlib.pyplot as plt
import numpy as np

'''
Raw eeg data files are approximately 1 GB each and contain data from all
4 blocks (PV0, WM0, PV1, WM1)
They have the following format ...
    %4d_EmoWorM.bdf % participant_number
'''

# define the data directory (this file is not found in the repository, there
# should be a local copy on your machine that points to the data)
fid = open('data_dir.path')
data_dir = fid.read().rstrip('\n')
fid.close()


class raw_eeg(mne.io.Raw):
    """Class to handle the raw eeg data

    Parameters
    ----------
    participant_id : int
        The id number for this participant
    """
    def __init__(self, participant_id):

        self.participant_id = participant_id
        self.bdf_fname = data_dir + '/RAWEEG/%d_EmoWorM.bdf' % participant_id

    def plot_event_channel(self):
        # read the raw bdf
        raw = mne.io.read_raw_edf(self.bdf_fname, preload=False,
                                  stim_channel='Status')
        # find the events
        x1, t1 = raw[-1]
        x1 = x1[0]
        # plot the events
        fig = plt.figure(figsize=(20, 100))
        ax = fig.add_subplot(111)
        ax.plot(t1, x1, 'b')
        ax.set_xticks(np.arange(0, t1.max(), 100))
        ax.set_ylim((0, 6e4))
        ax.set_xlabel('Time (seconds)')
        xlim = ax.get_xlim()
        ax.plot(xlim, [4096, 4096], 'r-')
        ax.plot(xlim, [8192, 8192], 'r-')
        ax.plot(xlim, [16384, 16384], 'r-')
        ax.plot(xlim, [32768, 32768], 'r-')

        # save the figure
        png_fname = self.bdf_fname.replace('.bdf', '.png')
        fig.savefig(png_fname)
        plt.close(fig)

if __name__ == "__main__":
    # make sure that the path exists
    this_eeg = raw_eeg(1001)
    assert path.exists(this_eeg.bdf_fname)
