#!/usr/local/bin/python2.6

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
###############################################################################################################
###############################################################################################################

def readFileName():
    
#
#--- read the names of fits files
#

#    os.system("ls -d /data/mta4/Deriv/*fits > /tmp/mta/zlist")
#    f     = open("/tmp/mta/zlist", "r")
    os.system("ls -d /data/mta4/Deriv/*fits > /tmp/zlist")
    f     = open("/tmp/zlist", "r")

    dlist = [line.strip() for line in f.readlines()]
    f.close()
#    os.system("rm /tmp/mta/zlist")
    os.system("rm /tmp/zlist")

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


