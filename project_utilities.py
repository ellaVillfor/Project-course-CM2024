# In the following file is all of the necessary functions to make the project work

import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs
import re
import scipy
from scipy.signal import find_peaks


#A EWMA filter funqtion syntax name_name()
def ewma_filter(values, alfa):
    #alfa = 0.5
    ewmaOutOld = 0 
    ewmaOut = [None]
    for i in values:
        ewmaOut.append(ewmaOutOld * alfa + values[i] * (1-alfa)) 
        ewmaOutOld = ewmaOut[i]
    
    return ewmaOut


def get_emg_data(filePath):
      
    #Open and reads the file with the EMG data to a long text string and saves it to rawData. Closes the file at the end.
    with open(filePath, 'r') as file:      #'opensignals_0007804b3c23_2024-09-09_15-04-53.txt'
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
    dataTable.append([None,None])
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


    return(dataTable)


def find_first_punch(dataTable, threshold):
    punch_found = False
    filtered_data = []

    for i, row in enumerate(dataTable):
        time, emg_signal = row
        
        # Skip None values
        if emg_signal is None:
            continue  # Gå till nästa rad om EMG är None

        # Include signal when threshold is reached
        if emg_signal > threshold:
            punch_found = True

        # If threshold has passed, save data
        if punch_found:
            filtered_data.append(row)

    # Kontroll in punch was found
    if not punch_found:
        print("Inget slag hittades över tröskelvärdet.")

    return filtered_data

def get_peak_values(dataTable):
    #use find peaks in dataTable --> we get index of peaks
    #put into new array = [EMG value, index]
    #send back 
    return 2
    


  
#Plotting the emg data and time
def plot_graf(dataTable):
 
    plt.plot([row[0] for row in dataTable],[row[1] for row in dataTable]) 
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.title('EMG-signal over time')
    plt.show()  

