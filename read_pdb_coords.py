#!/usr/bin/env python

import sys

def read_pdb_get_coords(pdbfile,chainl,atoml):
    '''get the xy coordinates of atoms from pdb chain and atomtype comma separated
    returns {chain:[atom#atomtype:[x,y,z]],atom#atomtype:[x,y,z]]}'''
    
    filename = pdbfile.split('/')[-1].split('.')[0]
    filedata = open(pdbfile,'r').readlines()
    if ',' in atoml:
        atoms = atoml.split(',')
    else:
        atoms = [atoml]
    if ',' in chainl:
        chains = chainl.split(',')
    else:
        chains = [chainl]
    
    chaindic = {}            #{chain{atomtypeatomno:[x,y,z]}}
    selected_atoms = []
    for i in filedata:
        line= i.split()
        if len(i) > 25:
            if i[:4] == 'ATOM': 
                chain = i[21]
                atomtype = i[13:15].replace(' ','')
                atomno = int(i[23:26])
                if atomtype in atoms and chain in chains:
                    try:
                        chaindic[chain][str(atomno)+atomtype] =[i[31:38],i[38:47],i[47:55]]
                    except:
                        print('ERROR? Found multiple sets of coords for atom: {0}{1}{2}'.format(chain,atomtype,atomno))
                        chaindic[chain] = {str(atomno)+atomtype:([i[31:38],i[38:47],i[47:55]])}
    return(chaindic)

### demo
print(read_pdb_get_coords(sys.argv[1],'A,B','CA,N'))