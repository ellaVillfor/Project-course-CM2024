import matplotlib.pyplot as plt
import json
import tkinter as tk
from tkinter import filedialog
import numpy as np
from tabulate import tabulate

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
    # Initialize the speed list with zero for the first time point
    speed = [0]

    # Iterate over acceleration data and integrate it to calculate speed
    for i in range(1, len(acc)):
        dt = timestamps[i] - timestamps[i - 1]  # Time difference between two points
        dv = acc[i] * dt  # Change in velocity (acceleration * time)
        #speed[i] = acc[i]*timestamps[i]
        speed.append(speed[-1] + dv)  # Add change in velocity to previous speed

    return speed

def calculate_position(acc, timestamps):
    # Initialize the position list with zero for the first time point
    position=[0]
    speed = [0]

    # Iterate over acceleration data and integrate it to calculate speed
    for i in range(1, len(acc)):
        dt = timestamps[i] - timestamps[i - 1]  # Time difference between two points
        dv = abs(acc[i]) * dt  # Change in velocity (acceleration * time)
        speed.append(speed[-1] + dv)  # Add change in velocity to previous speed

        dx = speed[i]*dt
        #position[i]= speed[i]*timestamps[i]
        position.append(position[-1] + dx)

    return position

# Function to plot acceleration and speed
def plot_acc_speed_and_position(timestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition):
    # Create subplots for acceleration and speed
    plt.figure(figsize=(12, 12))

    # Plot the acceleration data
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, xAcc, label='X Acceleration', color='r')
    plt.plot(timestamps, yAcc, label='Y Acceleration', color='g')
    plt.plot(timestamps, zAcc, label='Z Acceleration', color='b')
    plt.xlabel('Timestamps (seconds)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Acceleration Over Time')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)

    # Plot the speed data
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, xSpeed, label='X Speed', color='r', linestyle='--')
    plt.plot(timestamps, ySpeed, label='Y Speed', color='g', linestyle='--')
    plt.plot(timestamps, zSpeed, label='Z Speed', color='b', linestyle='--')
    plt.xlabel('Timestamps (seconds)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed Over Time')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)

    # Plot speed 
    plt.subplot(3,1,3)
    plt.plot(timestamps, xPosition, label='X Posittion', color='r', linestyle='--')
    plt.plot(timestamps, yPosition, label='Y Position', color='g', linestyle='--')
    plt.plot(timestamps, zPosition, label='Z Position', color='b', linestyle='--')
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

# Adjust timestamps to start from the first time Z-acceleration exceeds the threshold
adjustedTimestamps = adjust_timestamps_on_first_threshold(newTimestampsAcc, zAcc, threshold)

# Calculate speed for each axis
xSpeed = calculate_speed(xAcc, adjustedTimestamps)
ySpeed = calculate_speed(yAcc, adjustedTimestamps)
zSpeed = calculate_speed(zAcc, adjustedTimestamps)

# Calculate speed for each axis
xPosition = calculate_position(xAcc, adjustedTimestamps)
yPosition = calculate_position(yAcc, adjustedTimestamps)
zPosition = calculate_position(zAcc, adjustedTimestamps)

# Plot the acceleration and speed data
plot_acc_speed_and_position(adjustedTimestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition)

# # Prepare table
# table = list(zip(adjustedTimestamps, xAcc, xSpeed, xPosition))
# subheaders = ['Timestamps (s)', 'Acceleration (m/s^2)', 'Speed (m/s)', 'Position (m)']
# main_header = ["X"]
# table_with_main_header = [main_header] + [('', '', '', '')] + table  # Empty row after main header
# print(tabulate(table, headers=subheaders, tablefmt='grid'))

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
