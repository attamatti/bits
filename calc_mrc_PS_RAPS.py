#!/usr/bin/python

import glob
import sys
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import misc
import numpy as np
import pylab as py
import struct
from numpy import *

#------------- READ MRCs--------------
# from David Stokes
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
    input_image_dimension=(self.dim[1],self.dim[0])  #2D images assumed
    self.image_data=fromfile(file=input_image,dtype=imtype,count=self.dim[0]*self.dim[1]).reshape(input_image_dimension)
    input_image.close()
    return(self.image_data)
#---------------------------

#------------ calculate radial average--- image variable is 2D numpy array of FFT 
def azimuthalAverage(image,outname,center=None):
    print('calculating rotationally avgeraged 1D PS')
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (x.max()-x.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin
    
    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    raps = tbin / nr
    
    theimage = plt.plot(np.log10(raps))
    plt.savefig(outname)
    plt.close()
    
    return raps
#----------------------------------------------------------------


#----------- calculate Power spectrum---------------------------
def get_PS(image_in,outname):
    print('calculating FFT and PS')
    mrcim = mrc_image(image_in)
    image = read(mrcim)
    #image = plt.imread(image_in)           # for reading from tiffs instead of mrcs

    # fourier transform of the image.

    F1 = fftpack.fft2(image)
     
    # make pretty - put low res in center
    F2 = fftpack.fftshift( F1 )
     
    # Calculate 2D power spectrum
    ps2D = np.abs( F2 )**2
    
    theimage = plt.imshow(np.log10(ps2D),cmap='Greys_r')
    theimage.axes.get_xaxis().set_visible(False)
    theimage.axes.get_yaxis().set_visible(False)
    plt.savefig(outname)
    plt.close()
    
    return (ps2D)
#----------------------------------------------------------------

#--- calc distance on RAPS---------------------------------------
def calc_dist(ps2d,pxsize,resolution):
    """ given a resolution calculate its frequency
    on the RAPS
    """
    nyquist = 2*pxsize
    distance = ((np.shape(ps2d)[0]*.5)*nyquist)/resolution
    return(distance)
#-----------------------------------------------------------------

#--- calc resolution on RAPS---------------------------------------
def calc_reso(ps2d,pxsize,distance):
    """ given a distance calculate its frequency
    on the RAPS
    """
    nyquist = 2*pxsize
    resolution = ((np.shape(ps2d)[0]*.5)*nyquist)/distance
    return(resolution)
#-----------------------------------------------------------------


the_PS = get_PS(sys.argv[1],'testPS.png')
raps =  azimuthalAverage(the_PS,'testRAPS.png')
print raps.shape
print calc_reso(the_PS,1.04,2500)