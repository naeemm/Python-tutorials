import json
from pandas.io.json import json_normalize
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr

########################################################################
# open the file
filename = 'data.JSON'

with open(filename, 'r') as f:
    data = json.load(f)

######################################################################

# initialize variables
answering_time = []
is_correct = []
dt = []
corr = []
avgAT = []
stdAT = []
avgIC = []
stdIC = []

#############################################################################
# Browse data

for child in data:
    answering_time = []
    is_correct = []
    dt = []

    for session in child:

        temp = [at['answering_time'] for at in session]
        answering_time.extend(temp)

        temp = [at['is_correct'] for at in session]
        is_correct.extend(temp)

    corr.extend( pearsonr(answering_time, is_correct) )

    temp = np.array(answering_time)
    avgAT.append(temp.mean(axis=0))
    stdAT.append(temp.std(axis=0))

    temp = np.array(is_correct)
    avgIC.append(temp.mean(axis=0))
    stdIC.append(temp.std(axis=0))

###############################################################################
# extract correlation only , remove p values
corr = corr[0::2]

# normalize all values
avgAT /= max(avgAT)
stdAT /= max(stdAT)
avgIC /= max(avgIC)
stdIC /= max(stdIC)

###############################################################################


def draw_bar_plot(x, y, z, lblX, lblY, lblZ, graphTitle):

    n_groups = len(x)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.21
    opacity = 0.8

    # series 1
    rects1 = plt.bar(index, x, bar_width,
                     alpha=opacity,
                     color='b',
                     label=lblX)

    # series 2
    rects2 = plt.bar(index + bar_width, y, bar_width,
                     alpha=opacity,
                     color='y',
                     label=lblY)

    # series 3
    rects3 = plt.bar(index + 2 * bar_width, z, bar_width,
                     alpha=opacity,
                     color='r',
                     label=lblZ)

    plt.xlabel('Children index')
    plt.ylabel('Parameters')

    plt.title(graphTitle)

    plt.xticks(index + bar_width, (np.arange(n_groups)))
    plt.legend()

    plt.tight_layout()
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


# call the plotting
draw_bar_plot(avgAT, avgIC, corr, 'AT', 'IC', 'corr', 'All Children: Average (Answ.Time, Is.Correct, Correlation)')
draw_bar_plot(stdAT, stdIC, corr, 'AT', 'IC', 'corr', 'All Children: Stand deviation (Answ.Time, Is.Correct, Correlation)')

draw_bar_plot(avgAT, stdAT, corr, 'avg', 'std', 'corr', 'All Children: Answ. Time (Average, Std. deviation, Correlation)')
draw_bar_plot(avgIC, stdIC, corr, 'avg', 'std', 'corr', 'All Children: Is Correct (Average, Std. deviation, Correlation)')

###############################################################################


def draw_3d_plot(x,y,z, lblX, lblY, lblZ):

    fig = plt.figure(1)

    ax = fig.add_subplot(111, projection='3d')

    for c, m, zl, zh in [('r', 'o', min(x), max(x)), ('b', '^',  min(y), max(y))]:
        ax.scatter(x, y, z, c=c, marker=m)

    ax.set_xlabel(lblX)
    ax.set_ylabel(lblY)
    ax.set_zlabel(lblZ)
    title = 'All ' + str(len(x)) + ' Children'
    plt.title(title)
    plt.show()

#-----------------------------------------------------------------------------------------------------------------

draw_3d_plot(avgAT, avgIC, corr, 'Average (Ans.Time)', 'Average (Is.Correct)', 'Correlation (ans.time, is.correct)')

draw_3d_plot(stdAT, stdIC, corr, 'Std (Ans.Time)', 'Std (Is.Correct)', 'Correlation (ans.time, is.correct)')

###############################################################################

