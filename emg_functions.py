import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs
import re
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import filedialog

# Function to select file 
def select_emg_file():
    # Initialize Tkinter root (for file dialog)
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    emgFilePath = filedialog.askopenfilename(title="Select EMG file", filetypes=[("Text files", "*.txt")])
    with open(emgFilePath, 'r') as txt_file:
        rawData = txt_file.read()      
        txt_file.close     
        pass       
    return rawData

## Function: get_sample_rate
# The function identifies the sampling rate by reading in the data file
# Indata:
#   - file: with the EMG data
# Outdata:
#   - sampleRate: this is specifed in the file

def get_sample_rate(file):
    keywordSampleRate = '"sampling rate":'
    positionSampleRate = file.find(keywordSampleRate)

    if positionSampleRate != -1:
        dataStringSampleRate = file[positionSampleRate + len(keywordSampleRate):]
        
    else:
        print("ERROR: Word not found")

    keywordComma = ','
    positionComma = dataStringSampleRate.find(keywordComma)
    if positionComma != -1:
        sampleRateString = dataStringSampleRate[:positionComma]
    sampleRate = int(sampleRateString)
    return sampleRate


## Function: get_emg_data
# This function gets rid of header and cuts the data into single integers in order to be able to convert the raw data from a string to a list
# Indata:
#   - file: with the EMG data
#   - sampleRate
# Outdata:
#   - dataTable: integers that are put into a list

def get_emg_data(file,sampleRate):
    keyword = 'EndOfHeader'
    headerPosition = file.find(keyword)
    dataString = ""

    if headerPosition != -1:
        dataString = file[headerPosition + len(keyword):]
    else:
        print("ERROR: Word not found")
    
    pattern = r'\d+'
    dataNumbersString = re.findall(pattern, dataString)
    dataInt = [int(s) for s in dataNumbersString]
    dataTable = list_to_table(dataInt,sampleRate)
    return dataTable


## Function: list_to_table
# The function converts the list from the get_emg_data function to a table with 3 columns (index, a row with zeros and EMG data) in order to be able to turn the index to time
# Indata
#   - dataList: list with integers (called dataTable before)
#   - sampleRate 
# Outdata
#   - dataTable: the data converted to a table with 3 columns (time,arm emg data, chest emg data)

def list_to_table(dataList, sampleRate):
    #make the EMG data to a table instead of a list. Three columns [index, DI, EMG data]
    dataTable = []
    timeIndex = 0
    emgIndexArm = 2
    length = len(dataList)

    for i in range(length): 
        if timeIndex < (length-3):
            time =  dataList[timeIndex] /sampleRate    #turn the index of the emg data to the time
            emgDataArm = dataList[emgIndexArm]
            emgDataChest = dataList[emgIndexArm +1]
            dataTable.append([time,emgDataArm,emgDataChest])
            timeIndex +=4 
            emgIndexArm +=4
    return dataTable


## Function: find_first_punch
# With this function the user can find the first punch by manually checking where the punch starts and chose that value as a threshold. That will be where the graph starts.
# Indata
#   - dataTable: list with integers
#   - threshold: a value that the user manually choses 
# Outdata
#   - adjustedData: the graph is adjusted so that it starts where the first punch starts

def find_first_punch(dataTable, threshold):
    punchFound = False
    filteredData = []

    for i, row in enumerate(dataTable):
        time, emgSignal,_ = row

        if emgSignal is None:
            continue

        if emgSignal > threshold:
            punchFound = True

        if punchFound:
            filteredData.append(row)

    if not punchFound:
            print("No punch abobe threshold value was found.")

    # Adjusting the time for the data
    if len(filteredData) > 0:
        firstTime = filteredData[0][0]      
        adjustedData = [[row[0] - firstTime, row[1],row[2]] for row in filteredData]
    return adjustedData


# Function: apply_filter
def apply_filter(data, lowcut, highcut, fs, order = 5):

    b,a = bandpass_filter(lowcut, highcut, fs, order = order)
    y = filtfilt(b, a, data)    # Apply filter front sand back to avoid phase shift

    return y


## Function: bandpass_filter
# The function preforms a bandpass filter on the emg data.
# Indata:
#   - lowcut: The frequency threshold for lower frequencies
#   - highcut: The frequency threshold for higher frequencies
#   - fs: sampling rate of emg
#   - order: The order of the butterworthfilter. 1-3 provides softer slopes an 4-10 provides steeper slopes
# Outdata:
#   - b: numerator coefficients,determine how much of the input signal contributes to the current output sample.
#   - a: denominator coefficients, define how much of the previous output samples contribute to the current output sample
def bandpass_filter(lowcut, highcut, fs, order):
    nyquist = 0.5 * fs          # Nyquist frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')     # Create filtercoefficient
    return b, a


## Function: envelope_emg
# The function does a envelope extraction of the emg data. More information can be found here: https://github.com/UFTHaq/Extraction-Envelope-EMG-Signal-Myo-Armband-Forearm/blob/main/Extraction%20Envelope%20-%20EMG%20Forearm%20-%20UFTHaq%20GitHub.ipynb 
# Indata:
#   - emgData: a list of the emg data  
#   - window: how many values are looked apon when finding maximum values   
#   - sampleRate: The sampling rate of the emg 
# Outdata:
#   - maxEnvelopeValue: A list with the values extracted using the envelope method
#   - timeXValues: A list with the timestamps for each value in the maxEnvelopeValue
def envelope_emg(emgData,window,sampleRate):

    xValues = range(0, len(emgData), window)
    timeXValues = [x/sampleRate for x in xValues]
    maxEnvelopeValue =  [max(emgData[a:a+window]) for a in range(0, len(emgData), window)]

    return maxEnvelopeValue,timeXValues


## Function: get_muscle_time
# The function is to get the muscle activation time by looking at points above and below a threshold.
# Indata: 
#   - emgData: a list with values outlining the upper emg curve
#   - threshold: a muscle activation threshold for where we accept that a punch accures
#   - winow: the window that we look through values using the envalope method.
#   - sampleRate: the sampling rate of the emg
#   - diffThreshold: the threashold that we accept a muscle activation time difference for a punch to have. Differences under this threshold is not considered a punch.
# Outdata: 
#   - diffList: a list with the muscle time activation for every punch

def get_muscle_time(emgData,threshold,window,sampleRate,diffThreshold):
    startIndex = []
    endIndex = []
    diffList = []

    for index in range(len(emgData)):
        if emgData[index-1] < threshold and (emgData[index] == threshold or emgData[index] > threshold):
            startIndex.append(index)
    for index in range(len(emgData)):
        if emgData[index-1] > threshold and (emgData[index] == threshold or emgData[index] < threshold):
            endIndex.append(index)

    if len(startIndex) == len(endIndex):
        for index in range(len(startIndex)):
            diff = endIndex[index] - startIndex[index]
            if diff > diffThreshold:
                diffList.append((diff*window)/sampleRate)
    else:
        print('ERROR')
    return diffList

