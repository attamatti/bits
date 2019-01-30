#!/usr/bin/python
# generalized script for messing with starfiles


#------- function test if string is a number --------------------------#
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#-----------------------------------------------------------------------

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    for i in alldata:
        if '#' in i and '_rln' in i:
            labelsdic[i.split('#')[0]] = int(i.split('#')[1])-1
        print i.split()
        if len(i.split()) > 3:
            data.append(i.split())
        if len(i.split()) < 3:
            header.append(i.strip("\n"))
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

#------ function: write all of the numbers in the fortran format ---------------------------#
def make_pretty_numbers(dataarray):
    prettyarray = []
    for line in dataarray:
        linestr = ""
        for i in line:
            if is_number(i):
                count = len(i.split('.'))
                if count > 1:
                    i = float(i)
                    if len(str(i).split('.')[0]) > 5:
                        linestr= linestr+"{0:.6e} ".format(i)
                    else:
                        linestr= linestr+"{0:12.6f} ".format(i)
                else:
                    linestr= linestr+"{0: 12d} ".format(int(i))
            else:
                linestr= linestr+"{0} ".format(i)
        prettyarray.append(linestr)
    return prettyarray
#---------------------------------------------------------------------------------------------#



(labels,header,data) = read_starfile("newstar.star")

print labels

#
#
# Do stuff with the starfile contents here
# make the output of the modifications as an array of
# single values
# [x,x,x,x,x,x,x,x,x]
# [x,x,x,x,x,x,x,x,x]
# [x,x,x,x,x,x,x,x,x]
#



prettydata = make_pretty_numbers(data)
for i in header:
    print i
for i in prettydata:
    print i