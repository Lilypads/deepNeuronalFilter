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

def plotTimeDomainNumber(name,amplitude):
    time = np.linspace(0,len(amplitude),len(amplitude))
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(time,amplitude)
    pyplot.xlabel('Sample Number')
    pyplot.ylabel('Amplitude') 

total_recording = 9
participant = 1
date=["24Sep2021","30Sep2021","12Oct2021" ,"12Oct2021" ,"12Oct2021" ,"12Oct2021" ,"14Oct2021" ,"14Oct2021","19Oct2021", "28Oct2021", "1Nov2021", "1Nov2021", "3Nov2021", "12Nov2021", "16Nov2021" ] #for loading file

# directory of script file
print(os.path.abspath(os.path.dirname(sys.argv[0])))
# change current working directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
# check current working directory
print(os.getcwd())

counter=participant*4-3 #for export > index all participants' data to recording1-60
name=["stress3","clean","stress1","stress2"] #for publish open access GitLab

for i in range(total_recording):
    if participant<10:
        data = np.loadtxt('../participantData/participant00{}/00{}_{}_{}.tsv'.format(participant,participant,date[participant-1],i+1))
    else:
        data = np.loadtxt('../participantData/participant0{}/0{}_{}_{}.tsv'.format(participant,participant,date[participant-1],i+1))
    data[:,10] = np.arange(1,len(data[:,0])+1,1)  #replace column 10 with sampling number
    dataARRAY = data[:,[10,7,8,13]]  #or using filtered channels [10,11,12,13] #samplingNumber ECG+EMG EMGonly checkDigit
  
    print(dataARRAY[0,0])
    # plotTimeDomainNumber("Raw data",dataARRAY[:,2])

    save = [1,4,5,6] #4,11
    # save = [2,4,5,6] #3,5
    save = [3,4,5,6] #1,2,6  #3
    # save = [1,7,8,9] #7
    # save = [2,7,5,6] #8
    # save = [1,7,5,9] #9,15
    # save = [2,7,5,9] #12
    # save = [1,4,5,9] #14
    # save = [1,4,8,6] #10
    # save = [1,7,5,9] #13
        
    if i+1 in save:
        # np.savetxt('../pRecordingData/Recording{}.tsv'.format(counter), dataARRAY , delimiter ='\t', fmt=['%d','%f','%f','%d'])  #for export > index all participants' data to recording1-60
        # np.savetxt('../pRecordingData/forPublish/participant{}/{}.tsv'.format(participant,name[counter%4]), dataARRAY , delimiter ='\t', fmt=['%d','%f','%f','%d'])  #for publish open access GitLab
        # plotTimeDomainNumber("Raw data",dataARRAY[:,2])
        counter+=1

