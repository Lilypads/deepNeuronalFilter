#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:08:47 2021

@author: lilypads
"""
import matplotlib.pyplot as pyplot
import numpy as np
import os
import sys

# directory of script file
print(os.path.abspath(os.path.dirname(sys.argv[0])))
# change current working directory
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
# check current working directory
print(os.getcwd())

# close all plot windows    
# pyplot.close("all")

delayLineLength = 45
preFilterBuffer = 250

recording=4
data = np.loadtxt('../cppData/recording{}/lWeights_recording{}.tsv'.format(recording,recording))
data2 = np.loadtxt('../cppData/recording{}/remover_recording{}.tsv'.format(recording,recording))

pyplot.figure()
pyplot.plot(data[:,-1])
pyplot.title('Weight Change (learning)')
pyplot.xlabel('Sample Number')
pyplot.ylabel('Amplitude') 

pyplot.figure()
pyplot.plot(data2[2*delayLineLength+preFilterBuffer:len(data2)])
pyplot.title('Remover')
pyplot.xlabel('Sample Number')
pyplot.ylabel('Amplitude') 