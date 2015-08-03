import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# define the participants
pids = range(1001, 1039)
n_pid = len(pids)

# define the genders
genders = np.array(['M', 'F', 'F', 'F', 'F',
                    'F', 'F', 'M', 'M', 'M',
                    'M', 'F', 'F', 'F', 'M',
                    'M', 'F', 'M', 'M', 'M',
                    'F', 'F', 'F', 'M', 'M',
                    'F', 'F', 'F', 'M', 'F',
                    'F', 'M', 'F', 'M', 'F',
                    'M', 'M', 'M'])

# define the column names
col_names = ['date', 'pid', 'block_number', 'block_type', 'trial_number',
             'trial_match', 'trial_valence', 'image', 'cue', 'probe',
             'correct', 'rt']

# count the number in each group
group_totals = np.zeros((2, 2))
groups = []

# create an array to store valence data
X = np.zeros((n_pid, 2))

# open an output file for R
fid = open('anova.txt', 'w')
fid.write('player gender group valence block score' +
          ' d_prime mean_rt med_rt mot\n')

# loop through the participants
for n, pid, gender in zip(range(n_pid), pids, genders):

    # find the data file
    dfile = glob.glob("../ColorThresh/BHVDATA/%d*.txt" % pid)[0]

    # read the data file into numpy
    data = np.genfromtxt(dfile, dtype=None, names=col_names, delimiter=',')

    # determine the group
    if data[0]['block_type'] == 0:
        group = 'A'
        wm_blocks = [1, 3]
    else:
        group = 'B'
        wm_blocks = [0, 2]
    groups.append(group)

    # print pid, group, gender

    # update the group counts
    if gender == 'M' and group == 'A':
        group_totals[0, 0] += 1
    elif gender == 'M' and group == 'B':
        group_totals[0, 1] += 1
    elif gender == 'F' and group == 'A':
        group_totals[1, 0] += 1
    elif gender == 'F' and group == 'B':
        group_totals[1, 1] += 1
    else:
        raise ValueError('Unknown group and/or gender')

    # get the working memory data
    wm_data = data[data['block_type'] == 1]
    # get the valence scores
    for v in range(2):
        # get the data for this valence
        v_data = wm_data[wm_data['trial_valence'] == v]
        # compute the score
        score = v_data['correct'].sum()
        X[n, v] = score

        # fid.write('P%d %s %s V%d %d\n' % (pid, gender, group, v, score))
        # loop through the blocks
        for b, block in enumerate(wm_blocks):
            # get the data for this block
            b_data = v_data[v_data['block_number'] == block]
            # compute the score
            score = b_data['correct'].sum()
            # compute d prime
            # compute hit rate and false alarm rate
            hit_rate = b_data[b_data['trial_match'] == 1]['correct'].mean()
            fa_rate = 1 - b_data[b_data['trial_match'] == 0]['correct'].mean()
            # correct for 0 and 1
            hit_rate = min(hit_rate, 1-1./24)
            hit_rate = max(hit_rate, 1./24)
            fa_rate = min(fa_rate, 1-1./24)
            fa_rate = max(fa_rate, 1./24)
            d = stats.norm.ppf(hit_rate) - stats.norm.ppf(fa_rate)
            # calculate mean rt
            mean_rt = b_data['rt'].mean()
            med_rt = np.median(b_data['rt'])
            # calculate motivation index
            mi = (b_data['correct'] / b_data['rt']).mean()
            # record results
            fid.write('P%d %s %s V%d B%d %d %f %f %f %f\n' %
                      (pid, gender, group, v, b, score, d,
                       mean_rt, med_rt, mi))


# convert groups to an array
groups = np.array(groups)

# perform a t-test on scores
t, p = stats.ttest_rel(X[:, 0], X[:, 1])
print t, p

# plot the histogram
plt.hist(X[:, 0] - X[:, 1], np.arange(-5.5, 13.5))
plt.show()

# write differences to text file
out = np.zeros((n_pid, 2))
out[:, 0] = pids
out[:, 1] = X[:, 0] - X[:, 1]
np.savetxt('valence.txt', out, fmt='%d')

# close the output file
fid.close()
