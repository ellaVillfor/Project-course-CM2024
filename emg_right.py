import pandas as pd                  # import pandas-libary to prosess data in tabells
import matplotlib.pyplot as plt      # import matplotlib to create graphs

with open('opensignals_0007804b3c23_2024-09-09_15-04-53.txt', 'r') as file:     # opens the flie in read mode and saves it as 'file'
    theData = file.read()       # saves the data in the vaible as one long textstring
    print(theData)
    file.close
    pass        # close the file


# Reads the data form the file, skips the headers (first 10 lines)
data = pd.read_csv('opensignals_0007804b3c23_2024-09-09_15-04-53.txt', skiprows=range(3), sep='\t', header=None, names=['nSeq', 'DI', 'CH5'])
# data is a pandas DataFrame, it structures the files contents as a table with columns
# pd.read_csv reads the textfile into a DataFrame
# skiprows skips the first 3 rows (header info)
# sep='\t', determeds that the file is tab seperated (text format whose primary function is to store data in a table structure where each record in the table is recorded as one line of the text file)
# header=None determents that ther is no header in the file
# names defines names for the columns. nSeq is sequential number, DI is digital input, CH5 is the EMG signal


print(data.head())  # Shows the first rows in DataFrame

plt.plot(data['nSeq'], data['CH5'], label='EMG Signal', color='blue') 

plt.xlim([0, 30])
plt.ylim([0, 500])

plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('EMG-signal over time')
plt.legend()        # explaning label

plt.show()