#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  12 21:54:39 2021

@author: lilypads
"""

import matplotlib.pyplot as pyplot
import numpy as np
import os
import sys

total_recording = 12

# directory of script file
print(os.path.abspath(os.path.dirname(sys.argv[0])))
# change current working directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
# check current working directory
print(os.getcwd())

for i in range(total_recording):
    data = np.loadtxt('../RawRecordingData/ECG_12AUG2021_{}.tsv'.format(i+1))
    data[:,10] = np.arange(1,len(data[:,0])+1,1)
    dataARRAY = data[:,[10,11,12,13]]
    # print(dataARRAY[0,0])
    np.savetxt('../RecordingData/Recording{}.tsv'.format(i+1), dataARRAY , delimiter ='\t', fmt=['%d','%f','%f','%d'])
                      
def plotTimeDomainNumber(name,amplitude):
    time = np.linspace(0,len(amplitude),len(amplitude))
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(time,amplitude)
    pyplot.xlabel('Sample Number')
    pyplot.ylabel('Amplitude') 

# plotTimeDomainNumber("Raw data",dataARRAY[:,1])