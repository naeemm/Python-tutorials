import json
from pandas.io.json import json_normalize
from pprint import pprint
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
############################################################
# open the file
filename = 'data.JSON'

with open(filename, 'r') as f:
    data = json.load(f)

# print complete data
# pprint(data)

########################################################################
# 3D plot
def draw_3d_plot(x,y,z,i,lblX,lblY,lblZ):

    fig = plt.figure(i)

    ax = fig.add_subplot(111, projection='3d')

    x /= max(x)
    y /= max(y)
    z /= max(z)

    for c, m, zl, zh in [('r', 'o', min(x), max(x)), ('b', '^',  min(y), max(y))]:
        ax.scatter(x, y, z, c=c, marker=m)

    ax.set_xlabel(lblX)
    ax.set_ylabel(lblY)
    ax.set_zlabel(lblZ)
    title = 'Child: ' + str(i)
    plt.title(title)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

########################################################################
# initialize variable
answering_time = []
is_correct = []
dt = []

i = 0 # iterator

########################################################################
# Browse all data (in hierachical way: list within list upto dictionary

for child in data:
    answering_time = []
    is_correct = []
    dt = []

    for session in child:

        temp = [at['answering_time'] for at in session]
        answering_time.extend(temp)

        temp = [at['is_correct'] for at in session]
        is_correct.extend(temp)

        temp = [at['date'] for at in session]
        dt.extend(temp)

    x = np.copy(answering_time)
    y = np.copy(dt)
    z = np.copy(is_correct)
    #print ( min(x), max(x), min(y), max(y), min(z), max(z))
    i += 1
    draw_3d_plot(x,y,z, i, 'answering_time','date','is_correct' )


########################################################################
# Browse data for examination and understanding
def browse(data):
    for child in data:
        for session in child:
            for quiz in session:
                print(quiz['answering_time'], quiz['is_correct'], quiz['date'])

########################################################################
