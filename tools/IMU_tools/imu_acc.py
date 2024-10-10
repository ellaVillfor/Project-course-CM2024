import matplotlib.pyplot as plt
import json
import tkinter as tk
from tkinter import filedialog
import numpy as np
from tabulate import tabulate
import math
from scipy.signal import butter, filtfilt

g= 9.81 
# Initialize Tkinter root (for file dialog)
root = tk.Tk()
root.withdraw()  # Hide the main Tkinter window

# List to store the timestamps and data
newTimestampsAcc = []
xAcc = []
yAcc = []
zAcc = []
xSpeed = []
ySpeed = []
zSpeed = []
acc = []

#Set threashold for zacc where timestamp starts, from calibration
threshold=4

# Function to read the .json file
def read_json_file():
    filePath = filedialog.askopenfilename(title="Select JSON file", filetypes=[("JSON Files", "*.json")])
    with open(filePath, 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to extract accelerometer data from the JSON structure
def extract_acc_data(jsonDataAcc):
    # Clear global lists
    originalTimestampsAcc = []
    accDataPerTimestamp = []
    newTimestampsAcc.clear()
    xAcc.clear()
    yAcc.clear()
    zAcc.clear()

    # Iterate through each entry in the JSON data
    for entry in jsonDataAcc['data']:
        acc_data = entry['acc']
        timestamp = acc_data['Timestamp']  # Extract the timestamp
        originalTimestampsAcc.append(timestamp)  # Store the timestamp

        # Extract x, y, z values from ArrayAcc
        num_readings = len(acc_data['ArrayAcc'])
        accDataPerTimestamp.append(num_readings)  # Store the number of readings for each timestamp
            
        for acc_entry in acc_data['ArrayAcc']:
            xAcc.append(acc_entry['x'])
            yAcc.append(acc_entry['y'])
            zAcc.append(acc_entry['z'])

    # Convert timestamps to seconds
    start_time = originalTimestampsAcc[0]  # Initial timestamp for reference
    for i in range(len(originalTimestampsAcc)):
        originalTimestampsAcc[i] = (originalTimestampsAcc[i] - start_time) / 1000  # Convert to seconds

    # Process each pair of timestamps
    for i in range(len(originalTimestampsAcc) - 1):
        start_time = originalTimestampsAcc[i]
        end_time = originalTimestampsAcc[i + 1]

        # Determine number of readings for the current timestamp
        numberOfAccDataPerTimestamp = accDataPerTimestamp[i]
        
        # Calculate interval between new timestamps
        interval = (end_time - start_time) / numberOfAccDataPerTimestamp
        
        # Create equally spaced new timestamps
        for j in range(numberOfAccDataPerTimestamp):
            new_time = start_time + j * interval
            newTimestampsAcc.append(new_time)

    # Handle the last timestamp by estimating the interval
    for j in range(accDataPerTimestamp[-1]):
        new_time = originalTimestampsAcc[-1] + j * interval
        newTimestampsAcc.append(new_time)

    return newTimestampsAcc, xAcc, yAcc, zAcc

# Function of a low pass filter
def low_pass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyq  # Normalized cutoff frequency
    b, a = butter(order, normal_cutoff, btype='low', analog=False)  # Butterworth filter coefficients
    y = filtfilt(b, a, data)  # Apply the filter to the data
    return y

# Function to calculate acceleration
def calculate_acceleration(xAcc, yAcc, zAcc):
    acc = [0] * len(xAcc)
    for i in range(len(xAcc)):
        acc[i] = math.sqrt(pow(xAcc[i],2) + pow(yAcc[i],2) + pow(zAcc[i],2)) - g
        # acc[i] = math.sqrt(pow((xAcc[i]-xAcc[i-1]),2) + pow((yAcc[i]-yAcc[i-1]),2) + pow((zAcc[i]-zAcc[i-1]),2))
    return acc

# Function to adjust timestamps to start from when Z-acceleration exceeds threshold
def adjust_timestamps_on_first_threshold(newTimestampsAcc, zAcc, threshold):
    # Find the index where Z-acceleration first exceeds the threshold
    for i, z in enumerate(zAcc):
        if z > threshold:
            threshold_index = i
            break
    else:
        # If no value exceeds the threshold, return the original timestamps
        return newTimestampsAcc

    # Adjust timestamps to start from 0 when zAcc exceeds the threshold
    adjustedTimestamps = [(ts - newTimestampsAcc[threshold_index]) for ts in newTimestampsAcc]

    return adjustedTimestamps

# Function to calculate speed by integrating acceleration over time
def calculate_speed(acc, timestamps):
    # Initialize the speed list with the same shape as acceleration and starts with zero
    speed = np.zeros_like(acc)

    # Uses the trapezoidal integration method to calculate speed
    for i in range(1, len(acc)):
        speed[i] = speed [i-1] + np.trapz(acc[i-1:i+1], timestamps[i-1:i+1])
        # speed[i] = np.trapz(acc[i-1:i+1], timestamps[i-1:i+1])

    return speed

# Function to calculate speed by integrating acceleration over time
def calculate_speed_2(acc, timestamps):
    # Initialize the speed list with the same shape as acceleration and starts with zero
    speed = np.zeros_like(acc)

    # Uses the trapezoidal integration method to calculate speed
    for i in range(1, len(acc)):
        # speed[i] = speed [i-1] + np.trapz(acc[i-1:i+1], timestamps[i-1:i+1])
        speed[i] = np.trapz(acc[i-1:i+1], timestamps[i-1:i+1])

    return speed

# Function to calculate position by integrating speed over time
def calculate_position(speed, timestamps):
    # Initialize the position list with the same shape as speed and starts with zero
    position = np.zeros_like(speed)

    # Uses the trapezoidal integration method to calculate position
    for i in range(1, len(speed)):
        position[i] = position [i-1] + np.trapz(speed[i-1:i+1], timestamps[i-1:i+1])
        # position[i] = np.trapz(speed[i-1:i+1], timestamps[i-1:i+1])

    return position

# def calculate_position(acc, timestamps):
#     # Initialize the position list with zero for the first time point
#     position=[0]
#     speed = [0]

#     # Iterate over acceleration data and integrate it to calculate speed
#     for i in range(1, len(acc)):
#         dt = timestamps[i] - timestamps[i - 1]  # Time difference between two points
#         dv = abs(acc[i]) * dt  # Change in velocity (acceleration * time)
#         speed.append(speed[-1] + dv)  # Add change in velocity to previous speed

#         dx = speed[i]*dt
#         #position[i]= speed[i]*timestamps[i]
#         position.append(position[-1] + dx)

#     return position

# Function to plot acceleration and speed
def plot_acc_speed_and_position(timestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition, speed, position, acc):
    # Create subplots for acceleration and speed
    plt.figure(figsize=(12, 12))

    # Plot the acceleration data
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, xAcc, label='X Acceleration', color='r')
    plt.plot(timestamps, yAcc, label='Y Acceleration', color='g')
    plt.plot(timestamps, zAcc, label='Z Acceleration', color='b')
    plt.plot(timestamps, acc, label='Acceleration', color='y')
    plt.xlabel('Timestamps (seconds)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Acceleration Over Time')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)

    # Plot the speed data
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, xSpeed, label='X Speed', color='r', linestyle='-')
    plt.plot(timestamps, ySpeed, label='Y Speed', color='g', linestyle='-')
    plt.plot(timestamps, zSpeed, label='Z Speed', color='b', linestyle='-')
    plt.plot(timestamps, speed, label='Speed', color='y', linestyle='-')
    plt.xlabel('Timestamps (seconds)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed Over Time')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)

    # Plot position 
    plt.subplot(3,1,3)
    plt.plot(timestamps, xPosition, label='X Posittion', color='r', linestyle='-')
    plt.plot(timestamps, yPosition, label='Y Position', color='g', linestyle='-')
    plt.plot(timestamps, zPosition, label='Z Position', color='b', linestyle='-')
    plt.plot(timestamps, position, label='Position', color='y', linestyle='-')
    plt.xlabel('Timestamps (seconds)')
    plt.ylabel('Position')
    plt.title('Speed')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)

    # Show the plot
    plt.tight_layout()
    plt.show()

# Read, extract, and process accelerometer data
jsonDataAcc = read_json_file()
newTimestampsAcc, xAcc, yAcc, zAcc = extract_acc_data(jsonDataAcc)
# adjustedTimestamps, xAcc, yAcc, zAcc = extract_acc_data(jsonDataAcc)

# Adjust timestamps to start from the first time Z-acceleration exceeds the threshold
adjustedTimestamps = adjust_timestamps_on_first_threshold(newTimestampsAcc, zAcc, threshold)

# # Getting the frequency
# # Calculate the average time interval (in seconds)
# intervals = np.diff(adjustedTimestamps)  # Get the differences between consecutive timestamps
# average_interval = np.mean(intervals)  # Calculate the mean interval
# fs = 1 / average_interval if average_interval > 0 else 0  # Avoid division by zero
# cutoff = 1.2 # Cutoff frequency to use on the low pass filter

# # Apply filtering to accelerometer data
# xAcc_filtered = low_pass_filter(xAcc, cutoff, fs)
# cutoff = 3
# xAcc_filtered_2 = low_pass_filter(xAcc, cutoff, fs)
# yAcc_filtered = low_pass_filter(yAcc, cutoff, fs)
# zAcc_filtered = low_pass_filter(zAcc, cutoff, fs)

# # Calculate the acceleration using filtered data
# acc = calculate_acceleration(xAcc_filtered, yAcc_filtered, zAcc_filtered)

# # Calculate the speed using the filtered acceleration
# speed = calculate_speed(acc, adjustedTimestamps)

# # Calculate the position using the filtered speed
# position = calculate_position(speed, adjustedTimestamps)

# # Calculate speed for each axis using filtered data
# xSpeed = calculate_speed(xAcc_filtered, adjustedTimestamps)
# ySpeed = calculate_speed(yAcc_filtered, adjustedTimestamps)
# zSpeed = calculate_speed(zAcc_filtered, adjustedTimestamps)

# Calculate the acceleration
acc = calculate_acceleration(xAcc, yAcc, zAcc)

# Calculate the speed
# speed = calculate_speed(acc, adjustedTimestamps)

# Calculate the position using the filtered speed
# position = calculate_position(speed, adjustedTimestamps)

# Calculate speed for each axis
xSpeed = calculate_speed(xAcc, adjustedTimestamps)
# for i in range(1, len(xAcc)):
#     print(xAcc[i], ' - ', adjustedTimestamps[i], ' - ', xSpeed[i])
ySpeed = calculate_speed(yAcc, adjustedTimestamps)
zSpeed = calculate_speed(zAcc, adjustedTimestamps)
speed = calculate_speed(acc, adjustedTimestamps)
# speed = calculate_acceleration(xSpeed, ySpeed, zSpeed)

# Calculate speed for each axis
xPosition = calculate_position(xSpeed, adjustedTimestamps)
yPosition = calculate_position(ySpeed, adjustedTimestamps)
zPosition = calculate_position(zSpeed, adjustedTimestamps)
position = calculate_acceleration(xPosition, yPosition, zPosition)

# Plot the acceleration and speed data
# plot_acc_speed_and_position(adjustedTimestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition, speed)
plot_acc_speed_and_position(adjustedTimestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition, speed, position, acc)

# Prepare table
table = list(zip(adjustedTimestamps, xAcc, xSpeed, xPosition))
subheaders = ['Timestamps (s)', 'Acceleration (m/s^2)', 'Speed (m/s)', 'Position (m)']
main_header = ["X"]
table_with_main_header = [main_header] + [('', '', '', '')] + table  # Empty row after main header
print(tabulate(table, headers=subheaders, tablefmt='grid'))

# table = list(zip(adjustedTimestamps, yAcc, ySpeed, yPosition))
# headers = ['Timestamps (s)', 'Acceleration (m/s^2)', 'Speed (m/s)', 'Position (m)']
# main_header = ["Y"]
# table_with_main_header = [main_header] + [('', '', '', '')] + table 
# print(tabulate(table_with_main_header, headers=subheaders, tablefmt='grid'))

# table = list(zip(adjustedTimestamps, zAcc, zSpeed, zPosition))
# headers = ['Timestamps (s)', 'Acceleration (m/s^2)', 'Speed (m/s)', 'Position (m)']
# main_header = ["Z"]
# table_with_main_header = [main_header] + [('', '', '', '')] + table 
# print(tabulate(table_with_main_header, headers=subheaders, tablefmt='grid'))
