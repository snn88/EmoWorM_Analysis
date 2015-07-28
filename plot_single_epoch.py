import mne
import matplotlib.pyplot as plt
import numpy as np

def plot_epoch(participant=1001, block='PV0', condition='NEU', trial_number=0,
               scale=1e-5, save=False):

    '''
    participant - 4 digit id number
    block - string ('PV0', 'PV1', 'WM0', 'WM1')
    condition - string ('NEU' or 'NEG')
    trial_number - integer
    '''

    # construct the relavent file
    dfile = "./EPODATA/%d_%s-epo.fif" % (participant, condition)

    # read data into mne
    epo = mne.read_epochs(dfile, proj=False, add_eeg_ref=False)[trial_number]

    # get data
    X, = epo.get_data()
    X = X[:72]
    t = epo.times

    '''
    # compute ica
    n_pca = 10
    ica = mne.preprocessing.ICA(max_pca_components=n_pca)
    ica.fit(epo)
   
    # get each source 
    src = ica._transform_epochs(epo, True)
    
    # save the ica
    ica.save('%d_%s_%d-ica.fif' % (participant, condition, trial_number))
    '''
    # plot data
    #fig, ax = plt.subplots(2, figsize=(40, 20))
    fig, ax = plt.subplots(figsize=(40, 20))

    # plot each channel
    for n in range(72):
        # apply a dc offset
        ax.plot(t, X[n]-n*scale)

    '''
    for n in range(n_pca):
        ax[1].plot(t, src[n]-n*10)
    '''

    ax.set_xlim((t[0], t[-1]))
    ax.set_yticks(np.arange(0, -72, -1)*scale)
    ax.set_yticklabels(epo.ch_names[:72])

    # compute percentile
    mxmn = max(X.max(1)-X.min(1))

    # read aggregate data
    all_mxmn = np.genfromtxt('epo_nochan_max-min.txt')
    percentile = (all_mxmn < mxmn).mean()*100

    # construct title
    title = 'Participant: %d, Condition: %s, Trial: %d\n%.2e: %.2f Percentile' % \
            (participant, condition, trial_number, mxmn, percentile)
    ax.set_title(title)

    if save:
        figname = '%d_%s_%d.png' % (participant, condition, trial_number)
        fig.savefig(figname)

    return fig

if __name__ == "__main__":

    # loop through all of the particpants, conditions, and trials
    PIDS = range(1001, 1021)
    PIDS.pop(17)

    for pid in PIDS:
        for cond in ['PV-NEU', 'PV-NEG', 'WM-NEU', 'WM-NEG']:
            for tr in range(48):
    
                fig = plot_epoch(pid, cond, tr, save=True)
                plt.close(fig)
    
    plt.show()
