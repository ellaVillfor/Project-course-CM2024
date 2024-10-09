import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs
import re
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pylab as plt

#Open and reads the file with the EMG data to a long text string and saves it to rawData. Closes the file at the end.
with open('opensignals_0007804b3c23_2024-09-09_15-04-53.txt', 'r') as file:     
    rawData = file.read()      
    file.close
    pass        

#Getting sampling rate
keywordSampleRate = '"sampling rate":'
positionSampleRate = rawData.find(keywordSampleRate)

if positionSampleRate != -1:
    dataStringSampleRate = rawData[positionSampleRate + len(keywordSampleRate):]
    
else:
    print("ERROR: Word not found")

keywordComma = ','
positionComma = dataStringSampleRate.find(keywordComma)
if positionComma != -1:
    sampleRateString = dataStringSampleRate[:positionComma]
sampleRate = int(sampleRateString)

#Getting rid of the header on the rawData copy of the EMG file 
keyword = 'EndOfHeader'
position = rawData.find(keyword)

# Cuts the rawData string to get rid of the header
dataString = ""
if position != -1:
    dataString = rawData[position + len(keyword):]
else:
    print("ERROR: Word not found")

#Getting the numbers as strings from the raw data, put in a list
pattern = r'\d+'
dataNumbersString = re.findall(pattern, dataString)

#Translating dataNumbersString to integers, put in a list
dataInt = [int(s) for s in dataNumbersString]

#make the EMG data to a table instead of a list. Three columns [index, DI, EMG data]
dataTable = []
timeIndex = 0
emgIndex = 2
length = len(dataInt)

for i in range(length): 
    if timeIndex < (length-2):
        time =  dataInt[timeIndex] /sampleRate    #turn the index of the emg data to the time
        emgData = dataInt[emgIndex]
        dataTable.append([time,emgData])
        timeIndex +=3 
        emgIndex +=3

from project_utilities import find_first_punch
threshold = 35000
filterdSignal = find_first_punch(dataTable, threshold)

# Get the time for the filterd data
if len(filterdSignal) > 0:
    firstTime = filterdSignal[0][0]        # Get the fist timestamp
    adjustedData = [[row[0] - firstTime, row[1]] for row in filterdSignal]        # Adjust the timestamps to make the graph start at 0
    timeValues = [row[0] for row in adjustedData]         # Plot the adjusted data
    emgValues = [row[1] for row in adjustedData]


from filter import apply_filter
lowcut = 100
highcut = 450
filterdSignal = apply_filter(emgValues, lowcut, highcut, sampleRate)

window = 10
xValues = range(0, len(filterdSignal), window)
timeXValues = [(x*window)/sampleRate for x in xValues]
maxEmgValue =  [max(filterdSignal[a:a+window]) for a in range(0, len(filterdSignal), window)]


plt.figure(figsize = (18,4))
plt.plot(timeXValues, maxEmgValue, lw=1)

startIndex = []
endIndex = []
zoomThreshold = 3000
diffList = []

for index in range(len(maxEmgValue)):
    if maxEmgValue[index-1] < zoomThreshold and (maxEmgValue[index] == zoomThreshold or maxEmgValue[index] > zoomThreshold):
        startIndex.append(index)
for index in range(len(maxEmgValue)):
    if maxEmgValue[index-1] > zoomThreshold and (maxEmgValue[index] == zoomThreshold or maxEmgValue[index] < zoomThreshold):
        endIndex.append(index)

print(startIndex)
print(endIndex)

if len(startIndex) == len(endIndex):
    for index in range(len(startIndex)):
        diff = endIndex[index] - startIndex[index]
        if diff > 5:
            diffList.append((diff*window)/sampleRate)
else:
    print('ERROR')

print(diffList)


#Plotting the emg data and time
plt.plot(timeValues, filterdSignal)
plt.xlabel('index')
plt.ylabel('diff')
plt.title('Diff over time')
plt.show()
