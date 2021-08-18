#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:08:47 2021

@author: lilypads
"""
import matplotlib.pyplot as pyplot
import numpy as np

recording=9
data = np.loadtxt('../cppData/recording{}/lWeights_recording{}.tsv'.format(recording,recording))

pyplot.figure()
pyplot.plot(data[:,-1])