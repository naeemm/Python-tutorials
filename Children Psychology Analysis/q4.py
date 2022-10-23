import json
from pandas.io.json import json_normalize
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr
import pandas as pd
import statsmodels.api as sm
from pandas.tools.plotting import andrews_curves
import math
import os
import itertools
########################################################################
# open the file
filename = 'data.JSON'

with open(filename, 'r') as f:
    data = json.load(f)

######################################################################
# create a buffer directory
cwd = os.getcwd() # current working directory
bufferDir = cwd + '/buffer'
if not os.path.exists(bufferDir):
    os.makedirs(bufferDir)

######################################################################
# initialize variables
answering_time = []
is_correct = []
dt = []
corr = []
sess = []
childID = -1
corr = []
avgAT = []
avgIC = []
avgSess = []

######################################################################


def draw_curve_plot(dframe, cid, behav):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    # Andrews' curves
    andrews_curves(df, 'is_correct', ax=ax1)
    # multiline plot with group by
    for key, grp in dframe.groupby(['session']):
        ax2.plot(grp['date'], grp['answering_time'], label="" )
    plt.legend(loc='best')
    graphTitle = 'Child: ' + str(cid)
    graphTitle += ', Behaviour:' + behav
    plt.title(graphTitle)
    plt.xlabel('date')
    plt.ylabel('answering time')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

############################################################################


def draw_curve_plot2(dframe, cid, behav):
    fig, (ax1) = plt.subplots(nrows=1, ncols=1)
    # Andrews' curves
    andrews_curves(dframe, 'avgIC', ax=ax1)
    plt.legend(loc='best')
    graphTitle = 'Child: ' + str(cid)
    graphTitle += ', Behaviour:' + behav
    plt.title(graphTitle)
    plt.xlabel('session number')
    plt.ylabel('average correct answers')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

##############################################################################


def draw_curve_plot3(dframe, behav):
    fig, (ax) = plt.subplots(nrows=1, ncols=1)
    # multiline plot with group by
    for key, grp in dframe.groupby(['session']):
        ax.plot(grp['is_correct'], grp['answering_time'], label= "Child.{0:02d}".format(key) )
    plt.legend(loc='best')
    graphTitle = 'Behaviour: ' + behav
    plt.title(graphTitle)
    plt.xlabel('is_correct')
    plt.ylabel('answering time')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

##############################################################################

########################################################################
# Browse data

for child in data:
    answering_time = []
    is_correct = []
    dt = []
    sess = []
    childID += 1
    sessionID = 0
    avgAT = []
    avgIC = []
    avgSess = []

    for session in child:

        temp = [at['answering_time'] for at in session]
        answering_time.extend(temp)

        temp = [at['is_correct'] for at in session]
        is_correct.extend(temp)

        temp = [at['date'] for at in session]
        dt.extend(temp)

        # create a constant vector
        sessionID += 1
        temp = [sessionID]*len(temp)
        sess.extend(temp)

        temp = np.array(answering_time)
        avgAT.append(temp.mean(axis=0))

        temp = np.array(is_correct)
        avgIC.append(temp.mean(axis=0))

    corr.extend(pearsonr(answering_time, is_correct))
    # extract correlation only , remove p values
    df = pd.DataFrame({'session':sess, 'date':dt, 'answering_time':answering_time, 'is_correct':is_correct})
    df.to_pickle( bufferDir + '/' + str(childID) + '.pkl')

    avgSess = range ( len(avgIC) )

    df = pd.DataFrame({'avgIC': np.round(avgIC, 3), 'avgAT': avgAT, 'avgSess':avgSess})
    df.to_pickle( bufferDir + '/' + str(childID) + '.a.pkl')


##############################################################################

corr = corr[0::2]
avgIC = []
avgAT = []
childID = 0
sess = []
cutPoint = 0.15
totalSession = 10
####################################################################################

for i in range(len(corr)):
    df = pd.read_pickle(bufferDir + '/' + str(i) + '.a.pkl')
    avgIC.extend(df['avgIC'])
    avgAT.extend(df['avgAT'])
    # create a constant vector
    childID += 1
    temp = [childID] * totalSession
    sess.extend(temp)

###############################################################################

# repeat each correlation value ten times
uniqCr = corr
corr = list(itertools.chain.from_iterable(itertools.repeat(x, totalSession) for x in corr))

df = pd.DataFrame({'session':sess, 'answering_time':avgAT, 'is_correct':avgIC, 'corr':corr})

print(df)

# subsetting, find abnormal behaviour
dfN = df[df['corr'] >= cutPoint]
draw_curve_plot3(dfN, 'Normal')

dfA = df[df['corr'] < cutPoint]
draw_curve_plot3(dfA, 'Abnormal')

###############################################################################

#childID = 3
for i in range(childID):
    df = pd.read_pickle(bufferDir + '/' + str(i) + '.pkl')

    if uniqCr[i] >= cutPoint:
        behaviour = 'Normal'
    else:
        behaviour = 'Abnormal'
    draw_curve_plot(df, i+1, behaviour)

    df = pd.read_pickle(bufferDir + '/' + str(i) + '.a.pkl')
    draw_curve_plot2(df, i+1, behaviour)

###############################################################################

