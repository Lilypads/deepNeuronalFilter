#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:54:39 2021

@author: lilypads
"""

import matplotlib.pyplot as pyplot
import numpy as np
import os
import sys

total_recording = 12
fs = 250

delayLineLength = 60
preFilterBuffer = 250
    
# close all plot windows    
pyplot.close("all")

def doFourierTransform(data):
    # Plot Frequency Domain
    data_fft = np.fft.fft(data) 
    data_fourier = data_fft/len(data)         # Normalised Data
    data_amp = abs(data_fourier)
    data_dbs = 20*np.log10(abs(data_fourier))    # DB Conversion
    data_freq = np.linspace(0,fs,len(data))
    return data_amp, data_dbs,data_freq

def plotFourier(name,amp,freq):
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(freq,amp)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude')
    pyplot.xlim([0,fs/2])
    
def plotFourierdB(name,dbs,freq):
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(freq,dbs)
    pyplot.xlabel('Frequency(Hz)')
    pyplot.ylabel('Amplitude(dB)')
    pyplot.xlim([0,fs/2])
    
def plotTimeDomain(name,amplitude):
    time = np.linspace(0,len(amplitude)/fs,len(amplitude))
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(time,amplitude)
    pyplot.xlabel('Time(s)')
    pyplot.ylabel('Amplitude')
    
def plotTimeDomainNumber(name,amplitude):
    time = np.linspace(0,len(amplitude),len(amplitude))
    pyplot.figure()
    pyplot.title(name+' data')
    pyplot.plot(time,amplitude)
    pyplot.xlabel('Sample Number')
    pyplot.ylabel('Amplitude')    

def doAllStuff(recording_num):
    
    # select recording numbers
    recording=recording_num
    
    # directory of script file
    # print(os.path.abspath(os.path.dirname(sys.argv[0])))
    # change current working directory
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    # check current working directory
    # print(os.getcwd())
    
    #RAW_data = np.loadtxt('../Recording_Data/Recording{}.tsv'.format(recording))
    SIGNAL_data = np.loadtxt('../cppData/recording{}/signal_recording{}.tsv'.format(recording,recording))
    NOISE_data = np.loadtxt('../cppData/recording{}/noise_recording{}.tsv'.format(recording,recording))
    DNS_data = np.loadtxt('../cppData/recording{}/fnn_recording{}.tsv'.format(recording,recording))
    LMS_data = np.loadtxt('../cppData/recording{}/lmsOutput_recording{}.tsv'.format(recording,recording))
    LPLC_data = np.loadtxt('../cppData/recording{}/laplace_recording{}.tsv'.format(recording,recording))
    
    # remove buffer from DNS
    SIGNAL_data = SIGNAL_data[delayLineLength:len(SIGNAL_data)]
    NOISE_data = NOISE_data[delayLineLength:len(NOISE_data)]
    DNS_data = DNS_data[delayLineLength+preFilterBuffer+60:len(DNS_data)]
    LMS_data = LMS_data[delayLineLength:len(LMS_data)]
    LPLC_data = LPLC_data[delayLineLength:len(LPLC_data)]
    
    SIGNAL_amp, SIGNAL_dbs, SIGNAL_freq = doFourierTransform(SIGNAL_data)
    # plotTimeDomainNumber("Filtered Signal Time Domain",SIGNAL_data)
    # plotFourier("Filtered Signal",SIGNAL_amp, SIGNAL_freq)
    
    NOISE_amp, NOISE_dbs, NOISE_freq = doFourierTransform(NOISE_data)
    # plotTimeDomainNumber("Filtered Noise Time Domain",NOISE_data)
    # plotFourier("Filtered Noise",NOISE_amp, NOISE_freq)
        
    DNS_amp, DNS_dbs, DNS_freq = doFourierTransform(DNS_data)
    # plotTimeDomainNumber("Network Output Time Domain",DNS_data)
    # plotFourier("Network Output",DNS_amp, DNS_freq)
    
    LMS_amp, LMS_dbs, LMS_freq = doFourierTransform(LMS_data)
    # plotTimeDomain("LMS from fir1 Output Time Domain",LMS_data)
    # plotFourier("LMS from fir1 Output",LMS_amp, LMS_freq)
    
    LPLC_amp, LPLC_dbs, LPLC_freq = doFourierTransform(LPLC_data)
    # plotTimeDomain("Laplace Output Time Domain",LPLC_data)
    # plotFourier("Laplace Output",LPLC_amp, LPLC_freq)
    
    # plotTimeDomain("difference of SIGNAL and NOISE",SIGNAL_data-NOISE_data)
    # plotFourier("difference of SIGNAL and NOISE",SIGNAL_amp-NOISE_amp,SIGNAL_freq)
    # plotFourier("difference of Network Output and NOISE",DNS_amp-NOISE_amp,DNS_freq)
    
    # #try other methods
    # DNS_amp=LMS_amp
    # DNS_amp=LPLC_amp
    
    # find array index number during 0.5-100Hz
    fLEN = len(SIGNAL_amp)
    fStart =0.5
    fEnd = 100
    sStart = int(fStart/fs*fLEN)
    sEnd = int(fEnd/fs*fLEN)
    if recording%2 == 1:   #clean recordings are odd numbers
        sumSIGNAL_clean = np.sum(SIGNAL_amp[sStart:sEnd])
        #sumNOISE_clean = np.sum(NOISE_amp[sStart:sEnd])
        sumDNS_clean = np.sum(DNS_amp[sStart:sEnd])
        return sumSIGNAL_clean,sumDNS_clean
    else:               #noisy recordings are even numbers
        sumSIGNAL_noisy = np.sum(SIGNAL_amp[sStart:sEnd])
        # sumNOISE_noisy = np.sum(NOISE_amp[sStart:sEnd])
        sumDNS_noisy = np.sum(DNS_amp[sStart:sEnd])
        return sumSIGNAL_noisy,sumDNS_noisy

#run individually
# pick 2 recordings, one from clean one from noisy recordings
sumSIGNAL_clean,sumDNS_clean = doAllStuff(7)
sumSIGNAL_noisy,sumDNS_noisy = doAllStuff(8)

SNRBefore = sumSIGNAL_clean/ (sumSIGNAL_noisy-sumSIGNAL_clean)
SNRAfter = sumDNS_clean / (sumDNS_noisy-sumDNS_clean)
print(SNRBefore)
print(SNRAfter)

# #run in pairs
# i=1
# while(i<=total_recording):    
#     # pick 2 recordings, one from clean one from noisy recordings
#     sumSIGNAL_clean,sumDNS_clean = doAllStuff(i)
#     i+=1
#     sumSIGNAL_noisy,sumDNS_noisy = doAllStuff(i)
    
#     SNRBefore = sumSIGNAL_clean/ (sumSIGNAL_noisy-sumSIGNAL_clean)
#     SNRAfter = sumDNS_clean / (sumDNS_noisy-sumDNS_clean)
#     print("recording set:",i/2)
#     print(SNRBefore)
#     print(SNRAfter)
#     i+=1

# # plot greylayers
# total_layers = 11

# for layerIndex in range(1, total_layers+1, 1):
#     data = np.loadtxt('../cppData/recording{}/grayLayer{}__subject{}.csv'
#                       .format(recording, layerIndex, recording), dtype=float)
#     numNeurons = data.shape[0]
#     numInputs = data.shape[1]
#     # dataNormTemp = data - data.min()
#     dataNorm = data / abs(data).max()
#     fig1 = pyplot.figure('x recording{}, layer {}'.format(recording, layerIndex))
#     ax1 = fig1.add_subplot(111)
#     for i in range(dataNorm.shape[0]):
#         ax1.plot(dataNorm[i, :])
#         pyplot.title('recording{}'.format(recording))
#     pyplot.show()
#     fig = pyplot.figure('recording{}, layer {}'.format(recording, layerIndex))
#     ax = fig.add_subplot(111)
#     myImage = ax.imshow(dataNorm, cmap='bone', interpolation='none')
#     fig.colorbar(myImage, ax=ax)
#     pyplot.gca().set_yticks(np.arange(0, numNeurons, 2))
#     pyplot.gca().set_xticks(np.arange(0, numInputs, 5))
#     ax.set_aspect(aspect=2)
#     pyplot.title('recording{}'.format(recording))
#     pyplot.show()
#     # fig.savefig('../cppData' + fileName[myData] + '/recording' + str(recording)
#     #             + '/py_layer' + str(layerIndex) + '_gray_' + str(tri) + 'recording' + str(recording),
#     #             quality=10, format='eps', bbox_inches='tight')
#     # fig1.savefig('../cppData' + fileName[myData] + '/recording' + str(recording)
#     #              + '/py_layer' + str(layerIndex) + '_x_' + str(tri) + 'recording' + str(recording),
#     #              quality=10, format='eps', bbox_inches='tight')
    