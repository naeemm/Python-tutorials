import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import pandas as pd
import math
import os

########################################################################
# open the file
filename = 'data.JSON'

with open(filename, 'r') as f:
    data = json.load(f)

######################################################################
# create a buffer directory
cwd = os.getcwd()
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
allAT = []
allIC = []
allDT = []
allSess = []
allChildID = []

######################################################################
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

    corr.extend( pearsonr(answering_time, is_correct) )

    allAT.extend(answering_time)
    allDT.extend(dt)
    allIC.extend(is_correct)
    allSess.extend(sess)
    temp = [childID]* len(sess)
    allChildID.extend(temp)

df = pd.DataFrame({'allChildID':allChildID, 'session':allSess, 'date':allDT, 'answering_time':allAT, 'is_correct':allIC})
corr = corr[0::2]
cutPoint = 0.1
##############################################################################

#######
# There is no absolute pattern for Normal behaviour. The hypothesis rests upon correlation found
# between correct answers and answering time. Higher the positive correlation,
# more it is relevant to normal behaviour.
# We have taken highest correlation as the standard normal behaviour
# and compared it to other behaviour

# style/color
st = ['b-', 'r--', 'g-', 'y-', 'brown', 'gv-','salmon','magenta','black']
j = 0 # color index

for i in range(1,childID,1):

    j += 1
    j = 1 if j >= len(st) else j # loop for color/style

#    if math.fabs(corr[i]) < cutPoint:
    if corr[i] < cutPoint:

        # standard normal behaviour (15th child)
        dfA = df[df['allChildID'] == 14] # most correlated value
        x = dfA['date']
        y = dfA['answering_time']
        la = plt.plot(x, y, st[0], label='1 Normal')

        # abnormal behaviour
        dfA = df[df['allChildID'] == i]
        x = dfA['date']
        y = dfA['answering_time']
        la = plt.plot(x,y, st[j],label= str(i+2) + ' Abnormal')

        ll = plt.legend(loc='upper left')
        lx = plt.xlabel('date')
        ly = plt.ylabel('answering time')
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()
##########################################################################

