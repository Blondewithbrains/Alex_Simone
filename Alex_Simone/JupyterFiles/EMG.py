# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:44:19 2020

@author: stanzarella
"""

import numpy as np

def EMGcell2mat(SIG):

    r,c = np.shape(SIG)
    EMG = np.zeros([np.prod(np.shape(SIG)),np.shape(SIG[1][0])[1]])
    for ii in range(0,r):
        for jj in range(0,c):
            if (type(SIG[ii][jj]) is np.ndarray) & (np.shape(SIG[ii][jj])[1]>0):
                EMG[jj*r+ii,:] = SIG[ii][jj][0]
                
    return EMG