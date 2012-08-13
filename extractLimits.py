#!/usr/local/bin/python2.6

import sys
import os
import string
import re
import copy

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

###############################################################################################################
### extractLimit: create a limit data table os_limit_table                                                  ###
###############################################################################################################

def extractLimit():

    """
    read average and std values of each msid, compute lower and upper limits, and create limit data table
    Input: none, but extract a list from data_dir
    Output: data_dir/os_limit_table
    """
#
#--- read data set names from data directory
#
    cmd = 'ls ' + data_dir + '* > /tmp/ztemp'
    os.system(cmd)

    f    = open('/tmp/ztemp', 'r')
    data = [line.strip() for line in f.readlines()]
    f.close()
    os.system('rm /tmp/ztemp')
#
#--- print header
#
    outfile = data_dir + 'os_limit_table'
    fw   = open(outfile, 'w')
    fw.write('#\t\t\tLower Limit\t\tUpper Limit\t\tGroup\n')
    fw.write('#msid\t\t Red\tYellow\tYellow\tRed\n')
    fw.write('#-------------------------------------------------------\n')

#
#---- start printing limit values
#
    for ent in data:
        temp  = re.split(data_dir, ent)
        group = temp[1]                                     #---- group ID

        if ent == outfile:                                  #---os_limt_table is in the data directory, too; so ignore it
            pass
        else:
            f     = open(ent, 'r')
            msdat = [line.strip() for line in f.readlines()]
            f.close()
         
            colEnt = re.split('\s+|\t+', msdat[0])
            colLen  = len(colEnt)
            colName = []
#
#--- read msid names
#
            for ent in colEnt:
                if ent != 'std' and ent != '#time':
                    colName.append(ent)
    
#
#--- read average and std of each msid
#
            last = re.split('\s+|\t+', msdat[len(msdat) - 1])
            tcnt = len(last)
            avg = []
            sig = []
            for k in range(1, tcnt):
                if k % 2 == 0:
                    sig.append(float(last[k]))
                else:
                    avg.append(float(last[k]))
    

            fw.write('#\n') 
            for k in range(0, len(colName)):
#
#--- compute limits
#
                upperYellow = avg[k] + 4.0 * sig[k]
                upperRed    = avg[k] + 5.0 * sig[k]
                lowerYellow = avg[k] - 4.0 * sig[k]
                lowerRed    = avg[k] - 5.0 * sig[k]
    
                if len(colName[k]) < 8:
                    line = '%s\t\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%s\n' % (colName[k], lowerRed, lowerYellow, upperYellow, upperRed, group)
                else:
                    line = '%s\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%s\n'   % (colName[k], lowerRed, lowerYellow, upperYellow, upperRed, group)

                fw.write(line)
    
        fw.close()


#----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    extractLimit()
