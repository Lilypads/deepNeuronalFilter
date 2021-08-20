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
pyplot.close("all")

recording=12
data = np.loadtxt('../cppData/recording{}/lWeights_recording{}.tsv'.format(recording,recording))

pyplot.figure()
pyplot.plot(data[:,-1])