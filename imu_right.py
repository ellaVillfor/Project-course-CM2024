import matplotlib.pyplot as plt
import json

# # Output string
# OutputString = "Output"

# List to store the timestamps
newTimestampsAcc = []
originalTimestampsAcc = []
accDataPerTimestamp = []
newTimestampsGyro = []
originalTimestampsGyro = []
gyroDataPerTimestamp = []

# Lists to store the acceleration data
xAcc = []
yAcc = []
zAcc = []

# Lists to store the gyro data
xGyro = []
yGyro = []
zGyro = []

# Function to read the .json file
def read_json_file(filePathAcc):
    with open(filePathAcc, 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to read the .json file
def read_json_file(filePathGyro):
    with open(filePathGyro, 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to extract accelerometer data from the JSON structure
def extract_acc_data(jsonDataAcc):

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

    # Process each pair of timestamps
    for i in range(len(originalTimestampsAcc) - 1):
        start_time = originalTimestampsAcc[i]
        end_time = originalTimestampsAcc[i + 1]

        # Determine number of readings for the current timestamp
        numberOfAccDataPerTimestamp = accDataPerTimestamp[i]
        
        # Calculate interval between new timestamps
        interval = (end_time - start_time) / (numberOfAccDataPerTimestamp)
        
        # Create equally spaced new timestamps
        for j in range(0, numberOfAccDataPerTimestamp):
            new_time = start_time + j * interval
            newTimestampsAcc.append(new_time)
    
    # Generate new timestamps for the last timestamp using the values from the last one 
    # This is an estimation because we don't have a new timestamp to calculate the new timeintervals, so we just use the same as the last one
    for j in range(0, numberOfAccDataPerTimestamp):
        new_time = originalTimestampsAcc[len(originalTimestampsAcc) - 1] + j * interval
        newTimestampsAcc.append(new_time)

    return newTimestampsAcc, xAcc, yAcc, zAcc

# Function to extract gyro data from the JSON structure
def extract_gyro_data(jsonDataGyro):

    # Iterate through each entry in the JSON data
    for entry in jsonDataGyro['data']:
        acc_data = entry['gyroscope']
        timestamp = acc_data['Timestamp']  # Extract the timestamp
        originalTimestampsGyro.append(timestamp)  # Store the timestamp

        # Extract x, y, z values from ArrayGyro
        num_readings = len(acc_data['ArrayGyro'])
        gyroDataPerTimestamp.append(num_readings)  # Store the number of readings for each timestamp
            
        for acc_entry in acc_data['ArrayGyro']:
            xGyro.append(acc_entry['x'])
            yGyro.append(acc_entry['y'])
            zGyro.append(acc_entry['z'])

    # Process each pair of timestamps
    for i in range(len(originalTimestampsGyro) - 1):
        start_time = originalTimestampsGyro[i]
        end_time = originalTimestampsGyro[i + 1]

        # Determine number of readings for the current timestamp
        numberOfGyroDataPerTimestamp = gyroDataPerTimestamp[i]
        
        # Calculate interval between new timestamps
        interval = (end_time - start_time) / (numberOfGyroDataPerTimestamp)
        
        # Create equally spaced new timestamps
        for j in range(0, numberOfGyroDataPerTimestamp):
            new_time = start_time + j * interval
            newTimestampsGyro.append(new_time)
    
    # Generate new timestamps for the last timestamp using the values from the last one 
    # This is an estimation because we don't have a new timestamp to calculate the new timeintervals, so we just use the same as the last one
    for j in range(0, numberOfGyroDataPerTimestamp):
        new_time = originalTimestampsGyro[len(originalTimestampsGyro) - 1] + j * interval
        newTimestampsGyro.append(new_time)

    return newTimestampsGyro, xGyro, yGyro, zGyro


# Function to plot accelerometer data
def plot_acc_data(timestamps, xAcc, yAcc, zAcc):
    # Create a figure and axis
    plt.figure(figsize=(24, 6))

    # Plot the x, y, z accelerometer data
    plt.plot(newTimestampsAcc, xAcc, label='X Acceleration', color='r')
    plt.plot(newTimestampsAcc, yAcc, label='Y Acceleration', color='g')
    plt.plot(newTimestampsAcc, zAcc, label='Z Acceleration', color='b')

    # Add labels and title
    plt.xlabel('Timestamps')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Accelerometer Data Over Time')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

# Function to plot gyro data
def plot_gyro_data(timestamps, xGyro, yGyro, zGyro):
    # Create a figure and axis
    plt.figure(figsize=(24, 6))

    # Plot the x, y, z accelerometer data
    plt.plot(newTimestampsGyro, xGyro, label='X Gyro', color='r')
    plt.plot(newTimestampsGyro, yGyro, label='Y Gyro', color='g')
    plt.plot(newTimestampsGyro, zGyro, label='Z Gyro', color='b')

    # Add labels and title
    plt.xlabel('Timestamps')
    plt.ylabel('Gyroscope (XXXX)')
    plt.title('Gyroscope Data Over Time')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

# # Read, Extract and Plot Acc data

filePathAcc = 'right_arm_acc.json' 
jsonDataAcc = read_json_file(filePathAcc)
newTimestampsAcc, xAcc, yAcc, zAcc = extract_acc_data(jsonDataAcc)
print("Number of new_timestamps:", len(newTimestampsAcc))
print("Number of xAcc values:", len(xAcc))
print("Number of yAcc values:", len(yAcc))
print("Number of zAcc values:", len(zAcc))
plot_acc_data(newTimestampsAcc, xAcc, yAcc, zAcc)

# Read, Extract and Plot Gyro data

filePathGyro = 'right_arm_gyro.json' 
jsonDataGyro = read_json_file(filePathGyro)
newTimestampsAcc, xGyro, yGyro, zGyro = extract_gyro_data(jsonDataGyro)
print("Number of new_timestamps:", len(newTimestampsAcc))
print("Number of xGyro values:", len(xGyro))
print("Number of yGyro values:", len(yGyro))
print("Number of zGyro values:", len(zGyro))

plot_gyro_data(newTimestampsGyro, xGyro, yGyro, zGyro)


# # Output the results
# print("Timestamps:", timestamps)
# print("xAcc:", xAcc)
# print("yAcc:", yAcc)
# print("zAcc:", zAcc)


# # Create figure and subplots to simulate multiple canvases
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# # Setting titles for the canvases
# ax1.set_title("Acceleration Data")
# ax2.set_title("Gyro Data")
# ax3.set_title("Output Info")

# # Labels for the first canvas (Acceleration Data)
# ax1.set_xlabel('Time')
# ax1.set_ylabel('Acceleration (m/s²)')

# # Labels for the second canvas (Gyro Data)
# ax2.set_xlabel('Time')
# ax2.set_ylabel('Gyro (°/s)')

# # You can use ax3 to display some output or additional data
# ax3.text(0.5, 0.5, OutputString, horizontalalignment='center', verticalalignment='center', fontsize=12)
# ax3.axis('off')  # Turn off axis for this subplot

# # Show the figure (can be updated dynamically)
# plt.show()
