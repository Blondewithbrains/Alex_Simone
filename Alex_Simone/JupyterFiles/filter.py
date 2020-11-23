# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 15:38:41 2019

% This function filter the EMG channels. By default, a 4-th order
% Butterworth filter is applied to every channel between 20 Hz and 500 Hz.
% Input:
%   EMG:          data to be filtered
%   Fs :          sample frequency
%   order:        order of the filter
%   cut_freq:     [F_low F_high]
%   varargin:     tag 'env'
% Output:
%   EMG_F:        Filtered data
%
% Version 1.0: 09/10/2017
% Version 2.0: 20/12/2017 Simone Tanzarella

@author: tanza
"""
import numpy as np
from scipy import signal

def filterEMG2(EMG = [], Fs = [], order = 4, cutFreq = [20,500], *args):
    
    EMG_F = []
    
    if (not Fs) | ((type(Fs) is not float) & (type(Fs) is not int)):
        print('Not enough input arguments: missing signal or sample frequency')
        return EMG_F

    cutFreq = np.array(cutFreq)
    szcF = cutFreq.shape
    
    szEMG = EMG.shape
    
    if (not not szcF):
        if (max(szcF) > 2):
            print(' cut_freq must contain not more than two frequencies')
            return EMG_F
    
        elif (max(szcF) == 2):
            if (cutFreq[0] > cutFreq[1]):
                print('The second frequency is lower than the first, they will be reversed')
                cutFreq = np.flip(cutFreq)
            
            b, a = signal.butter(order, cutFreq/(Fs/2), 'band')
    else:
        b, a = signal.butter(order, cutFreq/(Fs/2))
    
    # Filter
    isCell = False
    if (len(szEMG) == 2) :
        if (not not EMG[0][1].shape ):
            isCell = True
            r,c = szEMG
            EMG_F = EMG
            for ii in range(0,r-1):
                for jj in range(0,c-1):
                    if (type(EMG[ii][jj]) is np.ndarray): #& (type(EMG[ii][jj][0]) is np.ndarray):
                        # if (type(EMG[ii][jj][0][0]) is float):
                        if (not not args) :
                            if (args[0] == 'env'):
                                EMG_F[ii][jj] = signal.filtfilt(b, a, np.absolute(EMG[ii][jj]))
                            else:
                                EMG_F[ii][jj] = signal.filtfilt(b, a, EMG[ii][jj])
                        else:
                            EMG_F[ii][jj] = signal.filtfilt(b, a, EMG[ii][jj])
        else:
            if (szEMG[0] > szEMG[1]):
                # EMG = EMG.T
                EMG = np.transpose(EMG)
        
    if (not isCell):
        if (not not args):
            if (args[0] == 'env'):
                EMG_F = signal.filtfilt(b, a, np.abs(EMG))
            else:
                EMG_F = signal.filtfilt(b, a, EMG)
        else:
            EMG_F = signal.filtfilt(b, a, EMG)

    
    return EMG_F
