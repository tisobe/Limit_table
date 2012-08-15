#!/usr/local/bin/python2.6

#################################################################################################################
#                                                                                                               #
#   createHtmlPage.py: create html pages to display trend plots under each group                                #
#                                                                                                               #
#           author: t. isobe (tisobe@cfa.harvard.edu)                                                           #
#                                                                                                               #
#           last update: Aug 15, 2012                                                                           #
#                                                                                                               #
#################################################################################################################

import sys
import os
import string
import re
import copy
import random

#
#--- define a temp file name
#

ztemp = '/tmp/ztemp' + str(random.randint(0,10000))


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
### createGroupHtmlPage: create html pages to display trend plots under each group                          ###
###############################################################################################################

def createGroupHtmlPage():

    """
    create html pages to display trend plots under each group
    input: none, but it will create plot lists from plot_dir
    output: html_dir/limit_trend.html and plot_dir/<gourp name>.html
    """

#
#--- read group names
#
    cmd = 'ls -d ' + plot_dir + '* >' + ztemp
    os.system(cmd)

    f     = open(ztemp, 'r')
    dlist = [line.strip() for line in f.readlines()]
    f.close()
    cmd = 'rm ' + ztemp
    os.system(cmd)

#
#--- create/update the top html page
#
    out_name1 = html_dir +  'limit_trend.html'
    fo = open(out_name1, 'w')

    line = '<!DOCTYPE html>\n<html>\n<head>\n<title>Limit Trend Page</title>\n</head>\n<body>\n\n'
    fo.write(line)
    line = '<h2 style="padding-bottom:20px">Limit Trend Plot</h2>\n\n'
    fo.write(line)
    line = '<ul>\n'
    fo.write(line)
#
#--- check each group
#
    for group in dlist:
        m1 = re.search('.html', group)                  #---- ignore the name ends with "html"
        if m1 is None:
            temp  = re.split(plot_dir, group)
            gname = temp[1]
#
#--- create indivisual html pages
#
            out_name1 =  group + '.html'
    
            line = '<li><a href="' + out_name1 + '">' + gname + '</a></li>\n'       #--- add line to the top html page
            fo.write(line)
    
            fo2 = open(out_name1, 'w')
    
            line = '<!DOCTYPE html>\n<html>\n<head>\n<title>' + gname + '</title>\n</head>\n<body>\n\n'
            fo2.write(line)
            line = '<h2> Group: ' + gname  + '</h2>\n\n'
            fo2.write(line)

            line = '<h3 style="padding-top:15px;padding-bottom:15px">Data Table: <a href="' + data_dir + gname + '">' + gname + '</a></h3>\n\n'
#
#--- find out plot names
#
            cmd  = 'ls ' + group + '/* >' + ztemp 
            os.system(cmd)
            f     = open(ztemp, 'r')
            plist = [line.strip() for line in f.readlines()]
            f.close()
            cmd = 'rm ' + ztemp
            os.system(cmd)
    
#
#--- create a table with plots:  two column format
#
            line = '<table border=0 cellpadding=5 cellspacing=5 style="padding-top:30px">\n'
            fo2.write(line)
    
            j = 0
            tot = len(plist)
            for ent in plist:
                m2 = re.search('png', ent)
                if m2 is not None:
                    temp  = re.split(group, ent)
                    pname = temp[1]
                    if j % 2 == 0:
                        line = '<tr><td><img src="./' + gname + '/' + pname + '"></td>\n'
                        fo2.write(line)
                        if j == tot - 1:
                            line = '<td>&#160</td></tr>\n'
                            fo2.write(line)
                    else:
                        line = '<td><img src="./' + gname + '/' +  pname + '"></td></tr>\n'
                        fo2.write(line)
                    j += 1
     
            line = '</table>\n'
            fo2.write(line)
            line = '</body>\n</html>\n'
            fo2.write(line)
     
            fo2.close()

    line = '</ul>\n<br /><br />\n<hr />\n'
    fo.write(line)

#
#--- Today's date 
#
    dtime = tcnv.currentTime('Display')

    line = 'Last Update: ' + dtime
    fo.write(line)

    line = '</body>\n</html>\n'
    fo.write(line)
    fo.close()



#----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    createGroupHtmlPage()
