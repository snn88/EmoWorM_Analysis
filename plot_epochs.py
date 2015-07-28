import mne
import matplotlib.pyplot as plt
import numpy as np

mne.set_log_level(False)

pids = range(1001, 1022)
blocks = ['PV0', 'PV1', 'WM0', 'WM1']
conditions = ['NEU', 'NEG']

n_trials = 24
n_channels = 72
n_participants = len(pids)
n_blocks = len(blocks)
n_conditions = len(conditions)
n_times = 4097

# construct output file of ranges
fout = open('ranges.txt', 'w')
fout.write('pid block valence trial channel range\n')

# spacing between channnels (DC offset)
scale = 1e-5

# loop through the participants
for p, pid in enumerate(pids):
    # loop through the blocks
    for b, block in enumerate(blocks):
        # loop through the conditions
        for c, condition in enumerate(conditions):

            # construct the filename
            dfile = "./EPODATA/%d_%s_%s-epo.fif" % \
                    (pid, block, condition)

            # read data into mne
            epo = mne.read_epochs(dfile, proj=False, add_eeg_ref=False)

            # get data
            epo_data = epo.get_data()
            t = epo.times
            
            # loop through the trials
            for m in range(n_trials):

                # get the trial data
                trial_data = epo_data[m, :72]

                '''
                # plot data
                fig, ax = plt.subplots(figsize=(40, 20))

                # plot each channel
                for n in range(72):
                    # apply a dc offset
                    ax.plot(t, trial_data[n]-n*scale)

                # set axes parameters
                ax.set_xlim((t[0], t[-1]))
                ax.set_yticks(np.arange(0, -72, -1)*scale)
                ax.set_yticklabels(epo.ch_names[:72])
                
                # construct title
                title = 'Participant: %d, Block: %s, Condition: %s, Trial: %d' % \
                        (pid, block, condition, m)
                ax.set_title(title)

                figname = './EPOPLOTS/%d_%s_%s_%d.png' % (pid, block, condition, m)
                fig.savefig(figname)

                plt.close(fig)
                '''

                for ch in range(72):
                    # compute range
                    rng = trial_data[ch].max()-trial_data[ch].min()
                    fout.write('%d %s %s %d %d %.4e\n' % (pid, block, condition, m, ch, rng))
 
                print pid, block, condition, m

# save the ranges
fout.close()

plt.show()
