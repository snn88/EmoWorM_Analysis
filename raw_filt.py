import mne
from os import path
import matplotlib.pyplot as plt
import numpy as np

'''
Filtered raw fif data files are contain data from 1 block (PV0, WM0, PV1, WM1)
They have the following format ...
    %4d_%s%d_%s:%sHz-raw.fif % (participant_number, condition, block_number,
                                l_freq, h_freq)
'''

# define the code directory
code_dir = path.dirname(__file__)

# define the data directory (this file is not found in the repository, there
# should be a local copy on your machine that points to the data)
fid = open(code_dir + '/data_dir.path')
data_dir = fid.read().rstrip('\n')
fid.close()


class raw_filt:

    """Class to handle filtered raw eeg data

    Parameters
    ----------
    participant_id : int
        The id number for this participant
    condition : str
        Passive view (PV) or Working memory (WM)
    block_number : int
        0 or 1
    l_freq : int
        The high pass
    h_freq : int
        The low pass
    """
    def __init__(self, participant_id, condition, block_number,
                 l_freq, h_freq):

        self.participant_id = participant_id
        self.condition = condition
        self.block_number = block_number
        self.raw_fname = data_dir + '/FILTFIF/%d_%s%d_%s:%sHz-raw.fif' % \
                                    (participant_id, condition, block_number,
                                     l_freq, h_freq)

    def _read_fif(self):
        # check to see if data has already been read
        if hasattr(self, 'raw'):
            return self.raw
        else:
            # read the raw fif
            raw = mne.io.read_raw_fif(self.raw_fname, preload=True, proj=False,
                                      add_eeg_ref=False)
            # store is attribute
            self.raw = raw
            return raw

    def plot_event_channel(self, show=False, save=True,
                           figsize=(20, 10)):
        # read the raw fif
        raw = mne.io.read_raw_fif(self.raw_fname, preload=False, proj=False,
                                  add_eeg_ref=False)
        # find the events
        x1, t1 = raw[-1]
        x1 = x1[0]
        # plot the events
        fig = plt.figure(figsize=figsize)
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

        if save:
            # save the figure
            png_fname = self.raw_fname.replace('.fif', '.png')
            fig.savefig(png_fname)
        if show:
            # display the figure
            plt.show()
        else:
            # close the figure
            plt.close(fig)

    def epoch_data(self):
        # read the raw data
        raw = self._read_fif()
        # get the events
        eve = mne.find_events(raw, mask=255)
        # epoch the data
        epo = mne.Epochs(raw, eve, [16384, 32768], -0.1, 0.5,
                         preload=True, proj=False, add_eeg_ref=False)
        # generate the epoch filename
        epo_fname = data_dir + '/EPODATA/%d_%s%d-epo.fif' % \
                               (self.participant_id, self.condition,
                                self.block_number)
        # save the epoch data
        epo.save(epo_fname)
        # store the epoch data filename
        self.epo_fname = epo_fname

if __name__ == "__main__":
    # make sure that the path exists
    this_eeg = raw_filt(1038, 'PV', 0, 1, 30)
    assert path.exists(this_eeg.raw_fname)
