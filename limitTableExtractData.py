#!/usr/local/bin/python2.6

#################################################################################################################
#                                                                                                               #
#   createLimitTable.py: create a table of averages over 6 month intevals from a fits file                      #
#                                                                                                               #
#       author: t. isobe (tisobe@cfa.harvard.edu)                                                               #
#                                                                                                               #
#       last update: Sep 07, 2012                                                                               #
#                                                                                                               #
#################################################################################################################

import sys
import os
import string
import re
import fnmatch
import numpy
import pyfits
import math

#
#--- reading directory list
#

path = './dir_list'
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
import convertTimeFormat    as tcnv
import mta_common_functions as mcf


###############################################################################################################
### createLimitTable: create a table of averages over 6 month intevals from a fits file                    ####
###############################################################################################################

def createLimitTable(file):

    """
    """
    m1    = re.search('/data/mta4/Deriv/grad', file)
    if m1 is not None:
        createTable2(file)
    else:
        createTable(file)


###############################################################################################################
### createTable: create a table of averages over 6 month intevals from a fits file                    ####
###############################################################################################################

def createTable(file):

    """
    this function read a fits file and create table of averages over 6 month intervals of each column
    and print them out.
    input:  file (fits file)
    output: ascii table of averages and standard deviations
    """
#
#--- create an output file and open for writing
#
    outName = makeOutFileName(file)
    outPath = data_dir + outName
    f = open(outPath, 'w')
#
#--- read fits file contents
#
    fdata    = pyfits.open(file)
    fbdata   =  fdata[1].data
    colNames = fdata[1].columns.names            #---- column names
    colLen   = len(colNames)                     #---- column length

#
#--- find "time" column position
#
    tpos = findTimeCol(colNames)

#
#--- print column names
#
    f.write('#time')
    for k in range(0, colLen):
        if k == tpos:
            pass
        else:
            temp = colNames[k].lower().replace('_avg','')
            temp = temp.replace('_', '')
            line = '\t%s\tstd' % (temp)
            f.write(line)

    f.write('\n')
#
#--- check each line until data runs out
#
    tot      = 0.0
    timeSum  = 0                                    #---- time span 
    dataSum  = [0 for x in range(colLen)]           #---- an array to save the sam of the values
    dataSum2 = [0 for x in range(colLen)]           #---- an array to save the sam of the value**2
    tbdata   = fbdata[0]
#    begining = tbdata[tpos]                         #---- start time of the interval
    begining = 63071999.0                           #---- start time of the interval Jan 1, 2000

    for tbdata in fbdata:
#
#--- the data occasionally have "NaN", and try:  line = '%6d\t' % (tbdata[tpos]) is a good way to skip the line
#
        try:
            if tbdata[tpos] > 63071999.0:
                line = '%6d\t' % (tbdata[tpos])         

                if timeSum <= 15778800:                     #---- 6 month in seconds, if less than that, keep accumurating
                    for k in range(0, colLen):
                            dataSum[k]  += tbdata[k]
                            dataSum2[k] += tbdata[k] * tbdata[k]
     
                    timeSum = tbdata[tpos] - begining
                    tot += 1.0
                else:
#
#--- if the data are accumurated for 6 months, compute averate and standard deviation, and print them out
#
                    line = '%6d\t' % (tbdata[tpos])
                    f.write(line)
     
                    for k in range(0, colLen):
                        if k == tpos:
                            pass
                        else:
                            davg = dataSum[k] / tot
                            dstd = math.sqrt(abs(dataSum2[k] / tot - davg * davg))
                            line = '%3.4f\t%3.4f\t' % (davg, dstd)
                            f.write(line)
    
                    f.write("\n")
    
                    tot      = 0.0
                    timeSum  = 0
                    dataSum  = [0 for x in range(colLen)]
                    dataSum2 = [0 for x in range(colLen)]
                    begining = tbdata[tpos]
        except:
            pass


    f.close()
    return outName

###############################################################################################################
### createTable2: create a table of averages over 6 month intevals from a fits file for grad data     ####
###############################################################################################################

def createTable2(file):

    """
    this function read a fits file and create table of averages over 6 month intervals of each column
    and print them out. Since gradablk.fits uses DOM for date, we need to handle differently.
    input:  file (fits file)
    output: ascii table of averages and standard deviations
    """
#
#--- create an output file and open for writing
#
    outName = makeOutFileName(file)
    outPath = data_dir + outName
    f = open(outPath, 'w')
#
#--- read fits file contents
#
    fdata    = pyfits.open(file)
    fbdata   =  fdata[1].data
    colNames = fdata[1].columns.names            #---- column names
    colLen   = len(colNames)                     #---- column length

#
#--- find "time" column position
#
    tpos = findTimeCol(colNames)

#
#--- print column names
#
    f.write('#time')
    for k in range(0, colLen):
        if k == tpos:
            pass
        else:
            temp = colNames[k].lower()
            m1   = re.search('dev', temp)
            if m1 is not None:
                f.write('\tstd')
            else:
                temp = colNames[k].lower().replace('_avg','')
                line = '\t%s' % (temp)
                f.write(line)

    f.write('\n')
#
#--- check each line until data runs out
#
    tot      = 0.0
    timeSum  = 0                                    #---- time span 
    dataSum  = [0 for x in range(colLen)]           #---- an array to save the sam of the values
    tbdata   = fbdata[0]
#    begining = tbdata[tpos]                        #---- start time of the interval
    begining = 366                                  #---- start time of the interval Jan 1, 2000

    for tbdata in fbdata:
#
#--- the data occasionally have "NaN", and try:  line = '%6d\t' % (tbdata[tpos]) is a good way to skip the line
#
        try:
            if tbdata[tpos] > 365.0:
                stime = tbdata[tpos] * 86400                #---- a day in second
                line = '%6d\t' % (stime)         

                if timeSum <= 183:                     #---- 6 month in day, if less than that, keep accumurating
                    for k in range(0, colLen):
                            if tbdata[k] != -99.0:
                                dataSum[k]  += tbdata[k]
     
                    timeSum = tbdata[tpos] - begining
                    if tbdata[k] != -99.0:
                        tot += 1.0
                else:
#
#--- if the data are accumurated for 6 months, compute averate and standard deviation, and print them out
#
                    stime = tbdata[tpos] * 86400 
                    line = '%6d\t' % (stime)
                    f.write(line)
     
                    for k in range(0, colLen):
                        if k == tpos:
                            pass
                        else:
                            davg = dataSum[k] / tot
                            line = '%3.4f\t' % (davg)
                            f.write(line)
    
                    f.write("\n")
    
                    tot      = 0.0
                    timeSum  = 0
                    dataSum  = [0 for x in range(colLen)]
                    begining = tbdata[tpos]
        except:
            pass


    f.close()
    return outName

###############################################################################################################
### makeOutFileName: isolate msid category from fits file name                                              ###
###############################################################################################################

def makeOutFileName(file):

    """
    isolate msid category from fits file name.
    example: /mta/.../aciseleca.fits to aciseleca
    input:  fits file name (with a full path)
    output: name
    """
#
#--- create an output file
#
    m1    = re.search('\/', file)
    if m1 is not None:
        atemp = re.split('\/', file)
        btemp = atemp[len(atemp)-1]
    else:
        btemp = file

    m1    = re.search('fits.gz', btemp)
    m2    = re.search('fits',    btemp)

    if m1 is not None:
        ctemp = re.split('\.fits.gz', btemp)
        return ctemp[0]
    elif m2 is not None:
        ctemp = re.split('\.fits',    btemp)
        return ctemp[0]
    else:
        return btemp


###############################################################################################################
### findTimeCol: find time column position                                                                 ####
###############################################################################################################

def findTimeCol(colNames):

    """
    find time column position 
    input:  a list of column Names
    output: a position of time columumn in int
    """

#
#--- find "time" column position
#
    tpos = 0
    for nam in colNames:
        if nam.lower() == 'time':
            break

        tpos += 1

    return tpos

#---------------------------------------------------------------------------------------------

if __name__ == "__main__":

    file = raw_input('Fits File Name: ')
    createLimitTable(file)


