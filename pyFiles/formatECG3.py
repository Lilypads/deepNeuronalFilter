#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  18 22:04:30 2021

@author: lilypads
"""

import matplotlib.pyplot as pyplot
import numpy as np
import os
import sys

# def cutFirstHalf(data):
#     index = int(len(data[:,0])/2)
#     output = data[:index,:]
#     return output

# def cutSecondHalf(data):
#     index = int(len(data[:,0])/2)
#     output = data[index:,:]
#     return output

def plotTimeDomainNumber(name,amplitude):
    time = np.linspace(0,len(amplitude),len(amplitude))
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(time,amplitude)
    pyplot.xlabel('Sample Number')
    pyplot.ylabel('Amplitude') 

total_recording = 9
participant = 8
date=["24Sep2021","30Sep2021","12Oct2021" ,"12Oct2021" ,"12Oct2021" ,"12Oct2021" ,"14Oct2021" ,"14Oct2021" ]

# directory of script file
print(os.path.abspath(os.path.dirname(sys.argv[0])))
# change current working directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
# check current working directory
print(os.getcwd())

counter=participant*4-3

for i in range(total_recording):
    data = np.loadtxt('../participantData/participant00{}/00{}_{}_{}.tsv'.format(participant,participant,date[participant-1],i+1))
    data[:,10] = np.arange(1,len(data[:,0])+1,1)
    dataARRAY = data[:,[10,11,12,13]]
    
  
    print(dataARRAY[0,0])
    # plotTimeDomainNumber("Raw data",dataARRAY[:,1])

    save = [1,4,5,6] #1,2,4,8
    # save = [2,4,5,6] #3,5,6
    # save = [1,7,8,9] #7
    if i+1 in save:
        np.savetxt('../pRecordingData/Recording{}.tsv'.format(counter), dataARRAY , delimiter ='\t', fmt=['%d','%f','%f','%d'])
        counter+=1
