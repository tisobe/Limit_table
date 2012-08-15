#!/usr/local/bin/python2.6

#################################################################################################################
#                                                                                                               #
#      LimitTableCreate.py: a control script to create limt trend data sets and their plots                     #
#                                                                                                               #
#           author: t. siboe (tisobe@cfa.harvard.edu)                                                           #
#                                                                                                               #
#           last update: Aug 14, 2012                                                                           #
#                                                                                                               #
#################################################################################################################

import sys
import os
import os.path
import string
import re
import fnmatch

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
import createLimitTable  as clt
import plotMsidLimits    as pml
import extractLimits     as ctbl
import createHtmlPage    as chtm

###############################################################################################################
### readFileName: a control script to create limit trend data sets and plots                               ####
###############################################################################################################

def readFileName():

    """
    a control script to create limit trend data sets and plots

    input: none, but will read house_keeping/data_list and eventually /data/mta4/Deriv/<msid group>.fits
    output: trend data (data_dir/<msid group name>), plot (plt_dir/<sid group name>/<msid>.png, and related html pages
    """
    
#
#--- read the names of fits files
#

#    os.system("ls -d /data/mta4/Deriv/*fits > /tmp/mta/zlist")
#    f     = open("/tmp/mta/zlist", "r")
#    dlist = [line.strip() for line in f.readlines()]
#    f.close()
#    os.system("rm /tmp/mta/zlist")

    indir = house_keeping + 'data_list'
    f     = open(indir, 'r')
    dlist = [line.strip() for line in f.readlines()]
#
#--- work on each fits files
#
    for file in dlist:
        print file
#
#--- extract limit values for msids in each group and print them out
#
        outName = clt.createLimitTable(file)

#
#--- check whether there is a directory for the group for creating plots
#
        out_path = plot_dir + outName
        if os.path.exists(out_path):
            pass
        else:
            cmd = 'mkdir ' + out_path
            os.system(cmd)
#
#--- plot the limit trend
#
        input = data_dir + outName 
        pml.msidLimitPlot(input, out_path)

#
#--- create a full table
#
    ctbl.extractLimit()
#
#--- create html to show trend plots
#
    chtm.createGroupHtmlPage()


#---------------------------------------------------------------------------------------------

if __name__ == "__main__":

    readFileName()


