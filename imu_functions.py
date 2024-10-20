import matplotlib.pyplot as plt
import json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import math
from scipy.signal import find_peaks

# Function to read the .json file
def read_json_file():
    # Initialize Tkinter root (for file dialog)
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    filePath = filedialog.askopenfilename(title="Select JSON file", filetypes=[("JSON Files", "*.json")])
    with open(filePath, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data

# Function to extract accelerometer data from the JSON structure
def extract_acc_data(jsonDataAcc):
    # List to store the timestamps and data
    newTimestampsAcc = []
    xAcc = []
    yAcc = []
    zAcc = []
    originalTimestampsAcc = []
    accDataPerTimestamp = []

    # Iterate through each entry in the JSON data
    for entry in jsonDataAcc['data']:
        accData = entry['acc']
        timestamp = accData['Timestamp']  # Extract the timestamp
        originalTimestampsAcc.append(timestamp)  # Store the timestamp

        # Extract x, y, z values from ArrayAcc
        numReadings = len(accData['ArrayAcc'])
        accDataPerTimestamp.append(numReadings)  # Store the number of readings for each timestamp
            
        for accEntry in accData['ArrayAcc']:
            xAcc.append(accEntry['x'])
            yAcc.append(accEntry['y'])
            zAcc.append(accEntry['z'])

    # Convert timestamps to seconds
    startTime = originalTimestampsAcc[0]  # Initial timestamp for reference
    for i in range(len(originalTimestampsAcc)):
        originalTimestampsAcc[i] = (originalTimestampsAcc[i] - startTime) / 1000  # Convert to seconds

    # This function is more complex because the sensor collects more than one value per timestamp
    # Because the  ovesense processes the data in batches - usually 8 values per timestamp
    # This part of the function checks how many acc data we have for each timestamp and divides the interval between
    # this and the next timestamp by the number of acc values

    # Process each pair of timestamps
    for i in range(len(originalTimestampsAcc) - 1):
        startTime = originalTimestampsAcc[i]
        endTime = originalTimestampsAcc[i + 1]

        # Determine number of readings for the current timestamp
        numberOfAccDataPerTimestamp = accDataPerTimestamp[i]
        
        # Calculate interval between new timestamps
        interval = (endTime - startTime) / numberOfAccDataPerTimestamp
        
        # Create equally spaced new timestamps
        for j in range(numberOfAccDataPerTimestamp):
            newTime = startTime + j * interval
            newTimestampsAcc.append(newTime)

    # Handle the last timestamp by estimating the interval
    for j in range(accDataPerTimestamp[-1]):
        newTime = originalTimestampsAcc[-1] + j * interval
        newTimestampsAcc.append(newTime)

    return newTimestampsAcc, xAcc, yAcc, zAcc

# Function to calculate acceleration
def calculate_acceleration(xAcc, yAcc, zAcc):
    # acc is always going to be > 0 so it won't have in consideration the direction but it is okay because we only want 
    # the peak value at the time the fist goes against the punching bag (we can see the acceleration coming almost to zero here)
    g = 9.81
    acc = [0] * len(xAcc)
    for i in range(len(xAcc)):
        acc[i] = math.sqrt(pow(xAcc[i],2) + pow(yAcc[i],2) + pow(zAcc[i],2)) - g 
    return acc

# Punch detection and max acceleration finder
def detect_punches_and_max_acc(timestamps, acc, windowSize, calibrationTimeThreshold=1):
    # Ensure timestamps is a numpy array
    timestamps = np.array(timestamps)

    # Filter out calibration by ignoring data before the calibration time threshold
    validDataIdx = np.where(timestamps > calibrationTimeThreshold)[0]
    filteredTimestamps = np.array(timestamps)[validDataIdx]
    filteredAcc = np.array(acc)[validDataIdx]
    
    # Detect peaks using find_peaks
    punchPeaks, _ = find_peaks(filteredAcc, height=100, distance=100)  # Adjust height and distance in accordance to each dataset
    # height = minimum height that a peak must have to be considered a valid peak
    # distance = minimum distance between consecutive peaks for the frequency used (f=833Hz), distance = 100 = 1/833 * 100 = 0.12 sec
    
    maxAccelerations = []
    # punch_intervals = []
    peakTimestamps = []
    
    for peak in punchPeaks:
        start = max(peak - windowSize, 0)
        end = min(peak + windowSize, len(filteredAcc) - 1)
        
        # Segment the punch from filtered_acc
        punchSegment = filteredAcc[start:end]
        
        # Find max value within the punch segment
        maxAcc = np.max(punchSegment)
        maxAccelerations.append(maxAcc)
        # punch_intervals.append((filtered_timestamps[peak], filtered_timestamps[end]))

        # Get the exact timestamp of the peak acceleration
        peakTimestamp = filteredTimestamps[peak]
        peakTimestamps.append(peakTimestamp)
    
    # Return detected punches and their max accelerations
    return punchPeaks, maxAccelerations, peakTimestamps

# Function to plot the acceleration and detected punches
def plot_punches_with_max_acc(timestamps, acc, punchPeaks, maxAccelerations, peakTimestamps):
    # This function plots a graph with the acceleration data and the peaks detected
    plt.figure(figsize=(12, 6))
    
    # Plot the combined acceleration
    plt.plot(timestamps, acc, label='Combined Acceleration', color='b')
    
    # Highlight detected punches
    plt.plot(peakTimestamps, maxAccelerations, 'rx', label='Detected Punches')
    
    # Annotate the max accelerations at punch peaks
    for i, peak in enumerate(punchPeaks):    
        plt.text(peakTimestamps[i], maxAccelerations[i] + 2, f"Max: {maxAccelerations[i]:.2f}", color='r', fontsize=9)

    
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Detected Punches and Max Acceleration')
    plt.legend()
    plt.grid(True)
    plt.xlim(left=0)
    plt.show()


# Function to adjust timestamps to start from when Z-acceleration exceeds threshold
def adjust_timestamps_on_first_threshold(newTimestampsAcc, zAcc, threshold):
    # This function is used to synchronize the time between the IMU and EMG data to make small check ups easier. 
    # In the beggining of the procedure we make a small touch in the EMG sensors that causes a movement for the IMU
    # Find the index where Z-acceleration first exceeds the threshold
    # we chose the z-axe because the movement is horizontal and in our movesense the vertical axe is the y
    for i, z in enumerate(zAcc):
        if z > threshold:
            thresholdIndex = i
            break
    else:
        # If no value exceeds the threshold, return the original timestamps
        return newTimestampsAcc

    # Adjust timestamps to start from 0 when zAcc exceeds the threshold
    adjustedTimestamps = [(ts - newTimestampsAcc[thresholdIndex]) for ts in newTimestampsAcc]

    return adjustedTimestamps

# Function to calculate speed by integrating acceleration over time
def calculate_speed(acc, timestamps):
    # This function would be used to calculate the speed using the trapezoidal method. 
    # We will not be using it but we left it here because it might be helpful for further projects
    # The sensor has an offset for each axis so to use this, we should put the acceleration back to zero before a punch
    # Initialize the speed list with the same shape as acceleration and starts with zero
    speed = np.zeros_like(acc)

    # Uses the trapezoidal integration method to calculate speed
    for i in range(1, len(acc)):
        speed[i] = speed [i-1] + np.trapz(acc[i-1:i+1], timestamps[i-1:i+1])

    return speed

# Function to calculate position by integrating speed over time
def calculate_position(speed, timestamps):
    # This function would be used to calculate the position using the trapezoidal method. 
    # We will not be using it but we left it here because it might be helpful for further projects
    # Initialize the position list with the same shape as speed and starts with zero
    position = np.zeros_like(speed)

    # Uses the trapezoidal integration method to calculate position
    for i in range(1, len(speed)):
        position[i] = position [i-1] + np.trapz(speed[i-1:i+1], timestamps[i-1:i+1])
        # position[i] = np.trapz(speed[i-1:i+1], timestamps[i-1:i+1])

    return position

# Function to plot acceleration and speed
def plot_acc_speed_and_position(timestamps, xAcc, yAcc, zAcc, xSpeed, ySpeed, zSpeed, xPosition, yPosition, zPosition, speed, position, acc):
    # Antoher function that will not be used
    # But what it does, it plots 3 graphs showing the acceleration, speed and position
    # For each graph we have the data according to each axe and one for all of them together (yellow)
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
