#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fourier transform using Python (version 3.5).

This code accompanies the book: The Fourier Transform: A Tutorial Introduction by James V Stone. 
https://jim-stone.staff.shef.ac.uk/Fourier

To run code, set testing to 0 to analyse data in supplied sound file or 1 to test code on synthetic data containing just two frequencies.

Note that this code is written for transparency, not speed. It does not use complex numbers. Instead the Fourier coefficients are found using sine and cosine functions. The corresponding MatLab code generated Figures 1.8a and 1.8b in the book (this Python code provides similar figures).


Spyder version: 4.1.5 None
Python version: 3.8.1 64-bit
Tested on mac OS 10.15.7 (Catalina)
@author: JimStone

Copyright: All except the sound files are public domain.
The sound files are sebinpubaudiIMG_1563.wav 
# and sebinpubaudiIMG_1563.m4a.

#############################
# Simple Fourier transform key variables
# 
# x       signal of N sampled values
# T       length of signal in seconds
# R       sampling rate in samples per second
# N       number of samples in signal
# nvec    vector of N ample numbers
# tvec    vector of N time values in seconds
# fundamental  vector of N elements 
# containing values from 0 to 2*pi =
# fundamental frequency
# fmax  maximum frequency in Hz, chosen by user 
# dt        interval in seconds between samples  = 1/R
# fmin    lowest frequency in Hz = 1/T
# nfrequencies  number of frequencies in transform
# Cs    vector of nfrequencies cosine coefficients
# Ds    vector of nfrequencies sine coefficients
# As    vector of nfrequencies Fourier amplitudes
# freqs vector of frequency values in Hz
#############################
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

testing = 0 
# set to 1 for synthetic data, and 0 for voice data.
fs = 10 # set fontsize for graphs.

###############################################
if testing: # make simple data to test program.    
    frequency = 500; 
    # insert this frequency Hz
    T = 0.5; # length of signal in seconds
    
    period = 1/frequency; # in seconds
    R = 44100; # set sampling rate, samples/s
    N = R*T; # number of samples in T seconds
    tvec = np.arange(0, N, 1)/R; 
    # time vector in units of seconds
    
    # make vector containg 1 frequency = 1/period.
    x1 = 2 * np.pi * tvec/period;
    
    # signal in which each interval of period 
    # seconds increases by 1.5*2*pi.
    x2 = 1.5*x1; # make sinusoids
    x = np.sin(x1);
    x = x + 0.5*np.sin(x2);    
else: # use data from sound file
    # set name of sound file
    fname = 'sebinpubaudiIMG_1563.wav';
    # read in data from file. 
    R, x = wavfile.read(fname)
    # set length of sound segment in seconds.
    segmentseconds = 0.5;
    N = int(R * segmentseconds);  
    # sample number at end of segmentseconds.
    # set start and end indices in data samples.
    xmin = 0; 
    xmax = xmin+N;
    x = x[xmin:xmax];
    T = N/R; # number of seconds in recording
# endif
###############################################

N = len(x); # number of samples.

# specify maximum frequency to be analysed here
fmax = 1000; # Hz

nvec = np.arange(0, N, 1);
# vector of N samples
tvec = np.arange(0, N, 1)/R;
# vector of N samples in units of seconds

# Plot first part of signal.
nforplot=500; # number of samples for graph.
plt.figure("Signal")
plt.clf()
plt.title("Signal",fontsize=fs)
plt.xlabel("Time (seconds)",fontsize=fs)
plt.ylabel("Amplitude",fontsize=fs)
plt.plot(tvec[0:nforplot],x[0:nforplot])
plt.show()

# make fundamental sinusoidal vector.
nvec = np.arange(0,N); # indices = 0->N-1
fundamental = nvec * 2 * np.pi / N; 
# fundamental now spans up to 2pi.

plt.figure("Fundamental")
plt.clf()
plt.title("Fundamental + one harmonic",fontsize=fs)
plt.xlabel("Time (seconds)",fontsize=fs)
plt.ylabel("Amplitude",fontsize=fs)
plt.plot(tvec,np.sin(fundamental),label="fundamental")
plt.plot(tvec,np.sin(2*fundamental),label="first harmonic")
plt.legend()
plt.show()
 
dt = 1/R; # interval between samples.
T = N/R;
fmin = 1.0/T; # lowest frequency in Hz.
# number of frequencies
nfrequencies = np.ceil(fmax/fmin);
nfrequencies = int(nfrequencies)

# make arrays to store Fourier coefficients.
Cs = np.arange(nfrequencies) * 0;
Ds = np.arange(nfrequencies) * 0;
# make array to store frequency values.
freqs = np.arange(nfrequencies) * 0;

###############################################
# Here is where the work gets done.
for n in range(1, nfrequencies):
    
    freq = fmin*n;
    freqs[n] = freq;
    
    # make cosine wave at frequency freq.
    cosinewave = np.cos(fundamental*n);
    # find inner product of sound with cosine wave.
    C = x.dot(cosinewave); 
    Cs[n-1] = C;
    
    # make sine wave at frequency freq.
    sinewave = np.sin(fundamental*n);
    # find inner product of sound with sine wave.
    D = x.dot(sinewave); 
    Ds[n-1] = D;
# work now done.
###############################################

# find amplitude of components, normalise by N.
As = ((Cs**2 + Ds**2) ** 0.5) / N

# Plot amplitude spectrum
plt.figure("Amplitude spectrum")
plt.clf()
plt.title("Amplitude spectrum",fontsize=fs)
plt.plot(freqs,As)
plt.xlabel("Frequency (Hz)",fontsize=fs)
plt.ylabel("Amplitude",fontsize=fs)
plt.show()

print('\nNumber of frequencies = ',nfrequencies)
print('\nFourier program completed.') 
############### 
# END OF FILE
################
