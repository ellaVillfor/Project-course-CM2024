import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs
import re
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pylab as plt

## Function: get_sample_rate
# Getting sampling rate by reading in the data file
# Indata:
#   - File: with the EMG data
# Outdata:
#   - Sample rate: this is specifed in the file

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
# Gets rid of header and cuts up the data in order to convert the raw data from a string to a list
# Indata:
#   - File: with the EMG data
#   - Sample rate
# Outdata:
#   - Data table: integers that are put into a list

def get_emg_data(file,sampleRate):
    #Getting rid of the header on the rawData copy of the EMG file 
    keyword = 'EndOfHeader'
    headerPosition = file.find(keyword)

    # Cuts the rawData string to get rid of the header
    dataString = ""
    if headerPosition != -1:
        dataString = file[headerPosition + len(keyword):]
    else:
        print("ERROR: Word not found")
    #Getting the numbers as strings from the raw data, put in a list
    pattern = r'\d+'
    dataNumbersString = re.findall(pattern, dataString)

    #Translating dataNumbersString to integers, put in a list
    dataInt = [int(s) for s in dataNumbersString]
    dataTable = list_to_table(dataInt,sampleRate)
    return dataTable
#----

def list_to_table(dataList, sampleRate):
    #make the EMG data to a table instead of a list. Three columns [index, DI, EMG data]
    dataTable = []
    timeIndex = 0
    emgIndex = 2
    length = len(dataList)

    for i in range(length): 
        if timeIndex < (length-2):
            time =  dataList[timeIndex] /sampleRate    #turn the index of the emg data to the time
            emgData = dataList[emgIndex]
            dataTable.append([time,emgData])
            timeIndex +=3 
            emgIndex +=3
    return dataTable


def find_first_punch(dataTable, threshold):
    punchFound = False
    filteredData = []

    for i, row in enumerate(dataTable):
        time, emgSignal = row

        # Skip None values
        if emgSignal is None:
            continue  # Go to next row if EMG is None

        # Include signal when threshold is reached
        if emgSignal > threshold:
            punchFound = True

        # If threshold has passed, save data
        if punchFound:
            filteredData.append(row)

    # Controll if punch was found
    if not punchFound:
            print("No punch abobe threshold value was found.")

    # Adjusting the time for the data
    if len(filteredData) > 0:
        firstTime = filteredData[0][0]        # Get the fist timestamp
        adjustedData = [[row[0] - firstTime, row[1]] for row in filteredData]        # Adjust the timestamps to make the graph start at 0

    return adjustedData
# Apply bandpass filter
def apply_filter(data, lowcut, highcut, fs, order = 5):

    b,a = bandpass_filter(lowcut, highcut, fs, order = order)
    y = filtfilt(b, a, data)    # Apply filter front sand back to avoid phase shift

    return y


# Bandpass filter
def bandpass_filter(lowcut, highcut, fs, order = 5):
    nyquist = 0.5 * fs          # Nyquist frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')     # Create filtercoefficient
    return b, a

def envalope_emg(emgData,window,sampleRate):

    xValues = range(0, len(emgData), window)
    timeXValues = [x/sampleRate for x in xValues]
    maxEnvalopeValue =  [max(emgData[a:a+window]) for a in range(0, len(emgData), window)]

    return maxEnvalopeValue,timeXValues

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

