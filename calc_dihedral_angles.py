#!/usr/bin/env python
import numpy as np
import math
import sys

# calculate the dihedral phi amd pai angles for a pdb file
# PHI is the predicted torsion angle C(i-1) N(i)  CA(i) C(i)   (degrees).
# PSI is the predicted torsion angle N(i)   CA(i) C(i)  N(i+1) (degrees).

if len(sys.argv) != 3:
    sys.exit('USAGE: calc_from_scratch.py <pdbfile> <chain>')



def calc_dihedral(p1,p2,p3,p4):
    # Calculate coordinates for vectors q1, q2 and q3
    q1 = np.subtract(p2,p1) # b - a
    q2 = np.subtract(p3,p2) # c - b
    q3 = np.subtract(p4,p3) # d - c
    
    # Calculate cross vectors
    q1_x_q2 = np.cross(q1,q2)
    q2_x_q3 = np.cross(q2,q3)

    # Calculate normal vectors
    n1 = q1_x_q2/np.sqrt(np.dot(q1_x_q2,q1_x_q2))
    n2 = q2_x_q3/np.sqrt(np.dot(q2_x_q3,q2_x_q3))

    """Function to calculate orthogonal unit vectors"""
    # Calculate unit vectors
    u1 = n2
    u3 = q2/(np.sqrt(np.dot(q2,q2)))
    u2 = np.cross(u3,u1)

    # Calculate cosine and sine
    cos_theta = np.dot(n1,u1)
    sin_theta = np.dot(n1,u2)
    
    # Calculate theta
    theta = -math.atan2(sin_theta,cos_theta) # it is different from Fortran math.atan2(y,x)
    theta_deg = np.degrees(theta)
    # Show results
    return(theta_deg)

file = sys.argv[1]
which_chain = sys.argv[2]
    
data = open(file,'r').readlines()
atoms = {}
atomcount = []
for line in data:
    if line[0:4] == 'ATOM' and line[13:17] in ('N   ','C   ','CA  ','O   ') and line[21] == which_chain:
        aaname ='{0}.{1}'.format(line[22:26],line[13:17]).strip()
        atoms[aaname] = np.array([float(line[30:38]),float(line[39:46]),float(line[47:54])]) 
        if int(line[22:26].strip()) not in atomcount:
            atomcount.append(int(line[22:26].strip()))
atomcount.sort()

phipsi = {}
for i in atomcount[1:-2]:
    ciminus1 = '{0}.C'.format(i-1)
    ni = '{0}.N'.format(i)
    cai = '{0}.CA'.format(i)
    ci = '{0}.C'.format(i)
    niplus1 = '{0}.N'.format(i+1)
    if ciminus1 in atoms and ni in atoms and cai in atoms and ci in atoms and niplus1 in atoms:
        phipsi[i] = [round(calc_dihedral(atoms[ciminus1],atoms[ni],atoms[cai],atoms[ci]),2),round(calc_dihedral(atoms[ni],atoms[cai],atoms[ci],atoms[niplus1]),2)]
    else:
        phipsi[i] = ['NaN']

for i in phipsi:
    print('{0},{1},{2}'.format(i,phipsi[i][0],phipsi[i][1]))
