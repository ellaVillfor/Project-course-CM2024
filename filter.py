import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pylab as plt


#A EWMA filter funqtion syntax name_name()
def ewma_filter(values):
    alfa = 0.5
    ewmaOutOld = 0 
    ewmaOut = [None]
    for i in values:
        ewmaOut.append(ewmaOutOld * alfa + i * (1-alfa)) 
        ewmaOutOld = ewmaOut[i]


# Bandpass filter
def bandpass_filter(lowcut, highcut, fs, order = 5):
    nyquist = 0.5 * fs          # Nyquist frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a


# Apply bandpass filter
def apply_filter(data, lowcut, highcut, fs, order = 5):
    b,a = bandpass_filter(lowcut, highcut, fs, order = order)
    y = filtfilt(b, a, data)
    return y

