import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs
import re

with open('opensignals_0007804b3c23_2024-09-09_15-04-53.txt', 'r') as file:     # opens the flie in read mode and saves it as 'file'
    rawData = file.read()       # saves the data in the vaible as one long textstring
    #print(theData)
    file.close
    pass        # close the file


# Reads the data form the file, skips the headers (first 10 lines)
#data = pd.read_csv('opensignals_0007804b3c23_2024-09-09_15-04-53.txt', skiprows=range(3), sep='\t', header=None, names=['nSeq', 'DI', 'CH5'])
# data is a pandas DataFrame, it structures the files contents as a table with columns
# pd.read_csv reads the textfile into a DataFrame
# skiprows skips the first 3 rows (header info)
# sep='\t', determeds that the file is tab seperated (text format whose primary function is to store data in a table structure where each record in the table is recorded as one line of the text file)
# header=None determents that ther is no header in the file
# names defines names for the columns. nSeq is sequential number, DI is digital input, CH5 is the EMG signal

#Getting rid of the header
keyword = 'EndOfHeader'
position = rawData.find(keyword)
dataString = ""
if position != -1:
    # Skär strängen från positionen efter ordet
    dataString = rawData[position + len(keyword):]
    
else:
    print("ERROR: Word not found")

#print(data.head())  # Shows the first rows in DataFrame
'''theDateTable = {
    "index" : [row[0] for row in theData[3: ]],
    "EMG" :  [row[0] for row in theData[3: ]]
}
print(theDateTable)'''
#Getting the numbers as strings from the raw data
pattern = r'\d+'
dataNumbersString = re.findall(pattern, dataString)

#Translating to int
dataInt = [int(s) for s in dataNumbersString]

#make to a table instead of a list 
dataTable = []
#dataTable.append(["index","zero","EMG"])
second = 1
third = 2
for first in dataInt: 
    firstValue =  dataInt[first]
    secondValue = dataInt[second]
    thirdValue = dataInt[third]
    dataTable.append([firstValue,secondValue,thirdValue])
    first +=3 
    second +=3
    third +=3

print(dataTable)

'''plt.plot(theData, theData[2], label='EMG Signal', color='blue') 

plt.xlim([0, 100])
plt.ylim([0, 4000])

plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('EMG-signal over time')
plt.legend()        # explaning label

plt.show()'''