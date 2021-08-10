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
    
def findRMS(data):
    summ = 0
    for i in range(len(data)):
        summ += data[i] * data[i]
    rms = np.sqrt(summ/len(data))
    return rms
    
# close all plot windows    
pyplot.close("all")
    
# select recording number
recording=9

# directory of script file
print(os.path.abspath(os.path.dirname(sys.argv[0])))
# change current working directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
# check current working directory
print(os.getcwd())

#RAW_data = np.loadtxt('../Recording_Data/Recording{}.tsv'.format(recording))
SIGNAL_data = np.loadtxt('../cppData/recording{}/signal_recording{}.tsv'.format(recording,recording))
NOISE_data = np.loadtxt('../cppData/recording{}/noise_recording{}.tsv'.format(recording,recording))
DNS_data = np.loadtxt('../cppData/recording{}/fnn_recording{}.tsv'.format(recording,recording))
LMS_data = np.loadtxt('../cppData/recording{}/lmsOutput_recording{}.tsv'.format(recording,recording))
LPLC_data = np.loadtxt('../cppData/recording{}/laplace_recording{}.tsv'.format(recording,recording))

# remove buffer from DNS
SIGNAL_data = SIGNAL_data[60:len(SIGNAL_data)]
NOISE_data = NOISE_data[60:len(NOISE_data)]
DNS_data = DNS_data[60:len(DNS_data)]
LMS_data = LMS_data[60:len(LMS_data)]
LPLC_data = LPLC_data[60:len(LPLC_data)]

SIGNAL_amp, SIGNAL_dbs, SIGNAL_freq = doFourierTransform(SIGNAL_data)
plotTimeDomainNumber("Filtered Signal Time Domain",SIGNAL_data)
plotFourier("Filtered Signal",SIGNAL_amp, SIGNAL_freq)

NOISE_amp, NOISE_dbs, NOISE_freq = doFourierTransform(NOISE_data)
plotTimeDomainNumber("Filtered Noise Time Domain",NOISE_data)
plotFourier("Filtered Noise",NOISE_amp, NOISE_freq)
    
DNS_amp, DNS_dbs, DNS_freq = doFourierTransform(DNS_data)
plotTimeDomainNumber("Network Output Time Domain",DNS_data)
plotFourier("Network Output",DNS_amp, DNS_freq)

LMS_amp, LMS_dbs, LMS_freq = doFourierTransform(LMS_data)
# plotTimeDomain("LMS from fir1 Output Time Domain",LMS_data)
# plotFourier("LMS from fir1 Output",LMS_amp, LMS_freq)

LPLC_amp, LPLC_dbs, LPLC_freq = doFourierTransform(LPLC_data)
# plotTimeDomain("Laplace Output Time Domain",LPLC_data)
# plotFourier("Laplace Output",LPLC_amp, LPLC_freq)

# plotTimeDomain("difference of SIGNAL and NOISE",SIGNAL_data-NOISE_data)
# plotFourier("difference of SIGNAL and NOISE",SIGNAL_amp-NOISE_amp,SIGNAL_freq)
# plotFourier("difference of Network Output and NOISE",DNS_amp-NOISE_amp,DNS_freq)

# find array index number during 0.5-100Hz
fLEN = len(SIGNAL_amp)
fStart = 0.5
fEnd = 100
sStart = int(fStart/fs*fLEN)
sEnd = int(fEnd/fs*fLEN)
sumSIGNAL = np.sum(SIGNAL_amp[sStart:sEnd])
sumNOISE = np.sum(NOISE_amp[sStart:sEnd])
sumDNS = np.sum(DNS_amp[sStart:sEnd])
SNRBefore = (sumSIGNAL - sumNOISE) / sumNOISE
SNRAfter = (sumDNS - sumNOISE) / sumNOISE
print(SNRBefore)
print(SNRAfter)

# # SNR (RMS method from time domain data)
# # recording 1 clean sample no. is 1500 - 2050, noiser sample no. is 1240 - 1320, 2850 - 2910
# # recording 11 clean sample no. is 2300 - 2900, noise sample no. is 5180 - 5240, 4815 - 4880
# SIGNAL_rms_clean = findRMS(SIGNAL_data[2300-60:2900-60])
# DNS_rms_clean = findRMS(DNS_data[2300-60:2900-60])
# LPLC_rms_clean = findRMS(LPLC_data[2300-60:2900-60])
# SIGNAL_rms_noise = findRMS(SIGNAL_data[5180-60:5240-60])
# DNS_rms_noise = findRMS(DNS_data[5180-60:5240-60])
# LPLC_rms_noise = findRMS(LPLC_data[5180-60:5240-60])
# SIGNAL_snr = 20*np.log10(SIGNAL_rms_clean/SIGNAL_rms_noise)
# DNS_snr = 20*np.log10(DNS_rms_clean/DNS_rms_noise)
# LPLC_snr = 20*np.log10(LPLC_rms_clean/LPLC_rms_noise)

# print("Signal RMS clean signal:", SIGNAL_rms_clean)
# print("Network RMS clean signal:", DNS_rms_noise)
# print("Laplace RMS clean signal:", LPLC_rms_noise)
# print("Signal RMS noise signal:", SIGNAL_rms_clean)
# print("Network RMS noise signal:", DNS_rms_noise)
# print("Laplace RMS noise signal:", LPLC_rms_noise)
# print("Signal SNR:", SIGNAL_snr, "dB")
# print("Network SNR:", DNS_snr, "dB")
# print("Laplace SNR:", LPLC_snr, "dB")


# //check data lengths
# print(len(SIGNAL_data))
# print(len(NOISE_data))
# print(len(DNS_data))
# print(len(LMS_data))
# print(len(LPLC_data))


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
    