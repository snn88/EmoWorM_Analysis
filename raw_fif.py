import mne
from os import path
import matplotlib.pyplot as plt
import numpy as np

'''
Raw fif data files are contain data from 1 block (PV0, WM0, PV1, WM1)
They have the following format ...
    %4d_%s%d-raw.fif % (participant_number, condition, block_number)
'''

# define the code directory
code_dir = path.dirname(__file__)

# define the data directory (this file is not found in the repository, there
# should be a local copy on your machine that points to the data)
fid = open(code_dir + '/data_dir.path')
data_dir = fid.read().rstrip('\n')
fid.close()


class raw_fif:

    """Class to handle the raw eeg data

    Parameters
    ----------
    participant_id : int
        The id number for this participant
    condition : str
        Passive view (PV) or Working memory (WM)
    block_number : int
        0 or 1
    """
    def __init__(self, participant_id, condition, block_number):

        self.participant_id = participant_id
        self.condition = condition
        self.block_number = block_number
        self.raw_fname = data_dir + '/RAWFIF/%d_%s%d-raw.fif' % \
                                    (participant_id, condition, block_number)

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

    def replace_electrodes(self):
        # read the replace file
        r = np.genfromtxt(code_dir + '/replace_electrodes.txt',
                          delimiter=',', dtype=None, names=True)
        # get the data for this file
        ix, = np.where(np.c_[r['participant'] == self.participant_id,
                             r['condition'] == self.condition,
                             r['block'] == self.block_number].all(1))
        # read the fif file
        raw = self._read_fif()
        # get the electrode indices
        bad_ix = raw.ch_names.index(r[ix]['bad'])
        new_ix = raw.ch_names.index(r[ix]['good'])
        # replace the bad electrodes
        raw._data[bad_ix] = raw._data[new_ix]
        # save the data
        raw.save(self.raw_fname, overwrite=True)

    def filter_data(self, l_freq, h_freq):
        # read the fif file
        raw = self._read_fif()
        # filter the data
        raw.filter(l_freq=l_freq, h_freq=h_freq, method='iir')
        # generate a new filename
        new_fname = self.raw_fname.replace('/RAWFIF/', '/FILTFIF/')
        new_fname = new_fname.replace('-raw.fif', '_%s:%sHz-raw.fif' %
                                      (l_freq, h_freq))
        # save the filtered data
        raw.save(new_fname, overwrite=True)
        # store the filtered filename
        self.filter_fname = new_fname

if __name__ == "__main__":
    # make sure that the path exists
    this_eeg = raw_fif(1038, 'PV', 0)
    assert path.exists(this_eeg.raw_fname)
