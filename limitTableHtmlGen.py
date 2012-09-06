#!/usr/local/bin/python2.6

#################################################################################################################
#                                                                                                               #
#   createHtmlPage.py: create html pages to display trend plots under each group                                #
#                                                                                                               #
#           author: t. isobe (tisobe@cfa.harvard.edu)                                                           #
#                                                                                                               #
#           last update: Sep 06, 2012                                                                           #
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

path = '/data/mta/Script/Limit_table/house_keeping/dir_list'
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

    line = '<!DOCTYPE html>\n<html>\n'
    fo.write(line)
    line = '<head>\n<title>MTA Limit Trend Page</title>\n'
    fo.write(line)
    line = '<link rel="stylesheet" type="text/css" href="/mta/REPORTS/Template/mta_monthly.css" />'
#    line = '<link rel="stylesheet" type="text/css" href="/data/mta4/www/REPORTS/Template/mta_monthly.css" />'
    fo.write(line)
    line = '</head>\n<body>\n\n'
    fo.write(line)
    line = '<h2 style="padding-bottom:20px">MTA Limit</h2>\n\n'
    fo.write(line)

    line = '<p style="padding-bottom:15px">Although there are Chandra operation range limit for each MSID, MTA group uses its own \n'
    fo.write(line)
    line = 'limit table for monitoring and trending purposes. \n'
    fo.write(line)
    line = '<p style="padding-bottom:15px">The limits for each MSID are created as following:</p>\n'
    fo.write(line)
    line = '<ul>\n'
    fo.write(line)
    line = '<li>The average and the standard deviation of each MSID are computed for 6 month periods for the entire period.</li>\n'
    fo.write(line)
    line = '<li>These averages and standard deviations are farther smoothed by taking past 2 year moving averages.</li>\n'
    fo.write(line)
    line = '<li><em style="color:yellow">Yellow Limits</em> are set at the center value (the average) plus or minus 4 standard deviation aways.</li>\n'
    fo.write(line)
    line = '<li><em style="color:red">Red Limits</em> are set t the center value (the average) plus or minus 5 standard deviation aways.</li>\n'
    fo.write(line)
    line = '<li>Most recent 6 month values of each MSID are taken as MTA Limit.</li>\n'
    line = '</ul><br /><br />'
    fo.write(line)

    line = '<p style="padding-bottom:25px">You can find the most recent MTA limit table at <a href="./Data/os_limit_table" target="blank">MTA Limit Table</a></p>.\n'
    fo.write(line)







#
#--- check each group
#
    line = '<h2 style="padding-bottom:20px">MTA Limit Trend</h2>\n\n'
    fo.write(line)

    line = '<p style="padding-bottom:40px">The following table lists trend plots of msids for each group. To see the plots, '
    fo.write(line)
    line = 'please click the group name. It will open the trend plot page of the group.  '
    fo.write(line)
    line = 'In each plot, the blue line indicates the (moving) average of the value of the msid, the yellow lines indicate lower and '
    fo.write(line)
    line = 'upper yellow limits, and red lines indicate lower and upper red limits.</p>\n\n'
    fo.write(line)


    line ='<div><table border=2 cellpadding=8 cellspacing=8 style="text-align:center;margin-left:auto;margin-right:auto">\n'
    fo.write(line)
    line = '<tr>'
    fo.write(line)

    ecnt = 0
    for group in dlist:
        m1 = re.search('.html', group)                  #---- ignore the name ends with "html"
        if m1 is None:
            temp  = re.split(plot_dir, group)
            gname = temp[1]
#
#--- create indivisual html pages
#
#            out_name1 =  group + '.html'
            out_name1 =  plot_dir + gname + '.html'
    
            line = '<td sytle="text-aligne:center"><a href="' + out_name1 + '">' + gname + '</a></td>\n'       #--- add line to the top html page
            fo.write(line)
#
#--- 4 entries per raw
#
            if ecnt > 2:
                ecnt = 0
                line = '</tr>\n'
                fo.write(line)
            else:
                ecnt += 1
#
#--- creating a html page for each group
#
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

    if ecnt == 0:
        line = '</table></div>\n<br /><br />\n<hr />\n'
        fo.write(line)
    else:
        for k in range(ecnt, 4):
            line = '<td>&#160</td>'
            fo.write(line)

        line = '</tr>\n</table></div>\n<br /><br />\n<hr />\n'
        fo.write(line)

#
#--- Today's date 
#
    dtime = tcnv.currentTime('Display')

    line = 'Last Update: ' + dtime
    fo.write(line)
    line = '<br /><br />If you have any questions about this page, please contact <a href="mailto:isobe@head.cfa.harvard.edu">isobe@head.cfa.harvard.edu</a>.'
    fo.write(line)

    line = '</body>\n</html>\n'
    fo.write(line)
    fo.close()



#----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    createGroupHtmlPage()
