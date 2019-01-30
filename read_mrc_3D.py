#!/usr/bin/python


# read an mrc file
from numpy import *
import numpy as np
import struct
import sys

#------------- READ MRCs--------------
# from David Stokes
# modified for 3D by Matt Iadanza

class mrc_image:
    def __init__(self,filename):
        self.numbytes1=56           # 56 long ints
        self.numbytes2=80*10          # 10 header lines of 80 chars each
        self.filename=filename

def read(self):
    input_image=open(self.filename,'rb')
    self.header1=input_image.read(self.numbytes1*4)
    self.header2=input_image.read(self.numbytes2)
    byte_pattern='=' + 'l'*self.numbytes1   #'=' required to get machine independent standard size
    self.dim=struct.unpack(byte_pattern,self.header1)[:3]   #(dimx,dimy,dimz)
    self.imagetype=struct.unpack(byte_pattern,self.header1)[3]  #0: 8-bit signed, 1:16-bit signed, 2: 32-bit float, 6: unsigned 16-bit (non-std)
    if (self.imagetype == 0):
        imtype='b'
    elif (self.imagetype == 1):
        imtype='h'
    elif (self.imagetype == 2):
        imtype='f4'
    elif (self.imagetype == 6):
        imtype='H'
    else:
        imtype='unknown'   #should put a fail here
        
    input_image_dimension=(self.dim[2],self.dim[1],self.dim[0])  #2D images assumed
    self.image_data=fromfile(file=input_image,dtype=imtype,count=self.dim[0]*self.dim[1]*self.dim[2]).reshape(input_image_dimension)
    input_image.close()
    return(self.image_data)
#---------------------------
         
         
#USAGE
mrcim = mrc_image(sys.argv[1])
image = read(mrcim)

print image
print image.shape
#print np.amax(image, axis=0)
#print image.sum(0)
#
#    returns numpy array with image values

