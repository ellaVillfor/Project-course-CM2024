import matplotlib.pyplot as plt
import json

# # Output string
# OutputString = "Output"

# List to store the timestamps
new_timestamps = []
original_timestamps = []
accDataPerTimestamp = []

# Lists to store the acceleration data
xAcc = []
yAcc = []
zAcc = []

# Lists to store the gyro data
xGyro = []
yGyro = []
zGyro = []

# Function to read the .json file
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to extract accelerometer data from the JSON structure
def extract_acc_data(json_data):

    # Iterate through each entry in the JSON data
    for entry in json_data['data']:
        acc_data = entry['acc']
        timestamp = acc_data['Timestamp']  # Extract the timestamp
        original_timestamps.append(timestamp)  # Store the timestamp

        # Extract x, y, z values from ArrayAcc
        num_readings = len(acc_data['ArrayAcc'])
        accDataPerTimestamp.append(num_readings)  # Store the number of readings for each timestamp
            
        for acc_entry in acc_data['ArrayAcc']:
            xAcc.append(acc_entry['x'])
            yAcc.append(acc_entry['y'])
            zAcc.append(acc_entry['z'])

    # Process each pair of timestamps
    for i in range(len(original_timestamps) - 1):
        start_time = original_timestamps[i]
        end_time = original_timestamps[i + 1]

        # Determine number of readings for the current timestamp
        numberOfAccDataPerTimestamp = accDataPerTimestamp[i]
        
        # Calculate interval between new timestamps
        interval = (end_time - start_time) / (numberOfAccDataPerTimestamp)
        
        # Create equally spaced new timestamps
        for j in range(0, numberOfAccDataPerTimestamp):
            new_time = start_time + j * interval
            new_timestamps.append(new_time)
    
    # Generate new timestamps for the last timestamp using the values from the last one 
    # This is an estimation because we don't have a new timestamp to calculate the new timeintervals, so we just use the same as the last one
    for j in range(0, numberOfAccDataPerTimestamp):
        new_time = original_timestamps[len(original_timestamps) - 1] + j * interval
        new_timestamps.append(new_time)

    return new_timestamps, xAcc, yAcc, zAcc


# Function to plot accelerometer data
def plot_acc_data(timestamps, xAcc, yAcc, zAcc):
    # Create a figure and axis
    plt.figure(figsize=(24, 6))

    # Plot the x, y, z accelerometer data
    plt.plot(new_timestamps, xAcc, label='X Acceleration', color='r')
    plt.plot(new_timestamps, yAcc, label='Y Acceleration', color='g')
    plt.plot(new_timestamps, zAcc, label='Z Acceleration', color='b')

    # Add labels and title
    plt.xlabel('Timestamps')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Accelerometer Data Over Time')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

# Extract the accelerometer data from the file

# Read, Extract and Plot

file_path = 'right_arm_acc.json' 
json_data = read_json_file(file_path)
new_timestamps, xAcc, yAcc, zAcc = extract_acc_data(json_data)
print("Number of new_timestamps:", len(new_timestamps))
print("Number of xAcc values:", len(xAcc))
print("Number of yAcc values:", len(yAcc))
print("Number of zAcc values:", len(zAcc))

plot_acc_data(new_timestamps, xAcc, yAcc, zAcc)


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
