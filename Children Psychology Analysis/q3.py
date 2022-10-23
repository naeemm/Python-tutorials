import json
import numpy as np
from collections import Counter
from discreteMarkovChain import markovChain
import pandas as pd
import matplotlib.pyplot as plt

########################################################################
# open the file
filename = 'data.JSON'

with open(filename, 'r') as f:
    data = json.load(f)

######################################################################

# initialize variables
is_correct = []
prob = []
sessID = 0
childID = 0

allCh = []
allSess = []
allProb = []
allStd = []
####################################################################


# Calculation of sequence probability
# using Markov chain property,
# p(s1, s2, s3,.....sn-1,sn) = p(sn-1|sn)... p(s3|s2) x p(s2|s1) x p(s1)
def calc_seq_prob(input_seq):

    # transition matrix
    tm = np.zeros((2,2))
    for (x,y), c in Counter(zip(input_seq, input_seq[1:])).iteritems():
        tm[x-1,y-1] = c

    P = tm/tm.sum(axis=1)[:,None]   # or ....... P = b/b.sum(axis=1, keepdims=True
    mc = markovChain(P)
    mc.computePi('linear') # 'linear', 'power', 'krylov', 'eigen'
    return mc.pi

####################################################################


# print the percentage of probability of next correct answer
def print_next_prob(cid, sid, ans,  pr):
    # we are interested only in correct answer
    # replace 1 by 0 if interested in wrong answer
    p = pr[0] if ans[0] == 1 else pr[1]

    msg = 'Child ID: ' + str(cid)
    msg += ', Session ID: ' + str(sid)
    msg += ', (next) correct answer probability'
    msg += ': ' + str(round(100 * p, 1)) + '%'
    print (msg)
    return p

#####################################################################


def draw_curve_plot3(dframe, std):

    fig, (ax) = plt.subplots(nrows=1, ncols=1)
    # multiline plot with group by
    for key, grp in dframe.groupby(['child']):
        ax.plot(grp['session'], grp['prob'], label= "Child.{0:02d}".format(key) + ":" + std[key-1] )
    plt.legend(loc='best')
    graphTitle =  'Children expected answer correctness '
    plt.title(graphTitle)
    plt.xlabel('session id')
    plt.ylabel('probability of next correct answer')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

#####################################################################

# Browse data
for child in data:
    answering_time = []
    is_correct = []
    dt = []
    childID +=1
    sessID = 0
    prob = []
    sess = []

    for session in child:

        sessID += 1

        is_correct = [at['is_correct'] for at in session]

        pr = calc_seq_prob(is_correct)
        p = print_next_prob(childID, sessID, is_correct, pr)
        prob.append(p)

        sess.append(sessID)

    # accumulate all data into a dataframe
    ch = [childID]*len(sess)
    allCh.extend(ch)
    allSess.extend(sess)
    allProb.extend(prob)
    allStd.append(np.std(prob, axis=0))

df = pd.DataFrame({'child':allCh, 'session':allSess, 'prob':allProb})

# cut across standard deviation of probability for ten session of each child
cutPoint = 0.1

# map all numeric standard deviation# cut across standard
# deviation of probability for ten session of each child
# into textual binary values
# defined by cutPoint
allBehav = []
for i in allStd:
    allBehav.append( 'Abnormal' if i > cutPoint else 'Normal')

# draw five children data only,
for i in np.arange(1,childID,5):
    # subset the dataframe
    dfS = df[ (df['child'] <= i+4) & (df['child'] >= i)]
    draw_curve_plot3(dfS, allBehav)

###############################################################################
