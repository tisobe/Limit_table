#!/usr/local/bin/python2.6

import sys
import os
import string
import re
import copy

#
#--- pylab plotting routine related modules
#

from pylab import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.lines as lines

#
#--- reading directory list
#

path = './house_keeping/dir_list'
f    = open(path, 'r')
data = [line.strip() for line in f.readlines()]
f.close()

for ent in data:
    atemp = re.split(':', ent)
    var  = atemp[1].strip()
    line = atemp[0].strip()
    exec "%s = %s" %(var, line)

#
#--- append path to a private folder
#

sys.path.append(mta_dir)
sys.path.append(bin_dir)

#
#--- converTimeFormat contains MTA time conversion routines
#
import convertTimeFormat as tcnv


####################################################################################################################
####################################################################################################################
####################################################################################################################

def msidLimitPlot(file, out_path):

    f    = open(file, 'r')
    data = [line.strip() for line in f.readlines()]
    f.close()

    colEnt = re.split('\s+|\t+', data[0])
    colLen  = len(colEnt)
    colName = []

    for ent in colEnt:
        if ent != 'std' and ent != '#time':
            colName.append(ent)

    time    = []
    for k in range(0, int(colLen/2)+1):
        exec("avg%d = []" % (k))
        exec("sig%d = []" % (k))

    total = 0
    for line in data:
        if total == 0:
            total += 1
        else:
            atemp    = re.split('\s+|\t+', line)

            yearDate = convertToYearDate(float(atemp[0]))
            time.append(yearDate)

            for k in range(1, colLen):
                k2 = int(k/2)
                if k % 2 == 0:
                    k2 -= 1
                    exec("sig%d.append(float(atemp[%d]))" % (k2, k))
                else:
                    exec("avg%d.append(float(atemp[%d]))" % (k2, k))

            total += 1

    for k in range(0, int(colLen/2)):
       col = colName[k]
       exec("davg = avg%d" % (k))
       exec("dsig = sig%d" % (k))

       plotPanel(col, time, davg, dsig, out_path)

####################################################################################################################
####################################################################################################################
####################################################################################################################

def plotPanel(col, time, davg, dsig, out_path):

    length = len(time)
    temp   = time
    temp.sort(key=float)
    xmin   = temp[0]
    xmax   = temp[length-1]
    xdiff  = xmax - xmin
    xmin  -= 0.1 * xdiff
    xmax  += 0.1 * xdiff
    xdiff  = xmax - xmin
    xbot   = xmin + 0.05 * xdiff

    upperYellow = []
    upperRed    = []
    lowerYellow = []
    lowerRed    = []

    for k in range(0, len(davg)):
        upperYellow.append(davg[k] + 4.0 * dsig[k])
        upperRed.append(davg[k] + 5.0 * dsig[k])
        lowerYellow.append(davg[k] - 4.0 * dsig[k])
        lowerRed.append( davg[k] - 5.0 * dsig[k])

    ymin  = min(lowerRed)
    ymax  = max(upperRed)
    ydiff = ymax - ymin

    if ydiff == 0:
        ymin -= 1
        ymax += 1
    else:
        ymin  -= 0.1 * ydiff
        ymax  += 0.1 * ydiff
    ydiff  = ymax - ymin
    ytop   = ymax - 0.12 * ydiff

#
#--- setting a few parameters
#

    plt.close('all')
    mpl.rcParams['font.size'] = 9
    props = font_manager.FontProperties(size=6)

    ax = plt.subplot(1,1,1)


#
#--- setting panel
#
    ax.set_autoscale_on(False)         #---- these three may not be needed for the new pylab, but 
    ax.set_xbound(xmin,xmax)           #---- they are necessary for the older version to set

    ax.set_xlim(xmin=xmin, xmax=xmax, auto=False)
    ax.set_ylim(ymin=ymin, ymax=ymax, auto=False)

#
#--- plotting
#
    plt.plot(time, davg,        color='blue',  lw=1, marker='+', markersize=1.5)
    plt.plot(time, upperYellow, color='yellow',lw=1, marker='+', markersize=1.5)
    plt.plot(time, lowerYellow, color='yellow',lw=1, marker='+', markersize=1.5)
    plt.plot(time, upperRed,    color='red',   lw=1, marker='+', markersize=1.5)
    plt.plot(time, lowerRed,    color='red',   lw=1, marker='+', markersize=1.5)

#
#--- naming
#
    plt.text(xbot, ytop, col)

#
#--- axis
#
    ax.set_ylabel(col)
    ax.set_xlabel('Time (Year)')
#
#--- set the size of the plotting area in inch (width: 5.0.in, height 3.0in)
#
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(5.0, 3.0)
#
#--- save the plot in png format
#
    name = out_path + '/' + col + '.png'
    plt.savefig(name, format='png', dpi=100)
    plt.close('all')

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def convertToYearDate(val):

    ntime = tcnv.convertCtimeToYdate(val)

    btemp = re.split(':', ntime)
    year  = float(btemp[0])
    ydate = float(btemp[1])
    hour  = float(btemp[2])
    mins  = float(btemp[3])

    chk   = int(0.25 * year)
    if chk == year:
        base = 366
    else: 
        base = 365

    yearDate = year + (ydate + hour/24.0 + mins/1440.0) / base

    return yearDate



#------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    file = raw_input("Data File Name: ")

    msidLimitPlot(file)
        
