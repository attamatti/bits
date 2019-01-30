#!/usr/bin/python
# generalized script for messing with starfiles
# updated for relion 3


###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile_new(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i:
            labelsdic[i.split()[0]] = labcount
            labcount +=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#


##### USE THE VERSION BELOW TO FIX MATT'S OLD SCRIPTS THAT ARE BROKEN BY RELION 3
#### Deals with the bug tha the original script had a space after every label name
###
##
##
##
###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#


(labels,header,data) = read_starfile("micrographs_ctf.star")
(labels2,header2,data2) = read_starfile_new("micrographs_ctf.star")


#### testing and error checking
lkeys = labels.keys()
l2keys = labels2.keys()
l2keys.sort()
lkeys.sort()

for i in zip(lkeys,l2keys):
    print i

for i in lkeys:
    print labels[i],labels2[i.replace(' ','')]

print data[-1]
print data2[-1]

print data[0]
print data2[0]

print (header[0],header[-1])
print (header2[0],header2[-1])


