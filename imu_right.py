import matplotlib.pyplot as plt
import json

# Output string
OutputString = "Output"

# List to store the timestamps
timestamps = []

# Lists to store the acceleration data
xAcc = []
yAcc = []
zAcc = []

# Lists to store the gyro data
xGyro = []
yGyro = []
zGyro = []

# Function to extract accelerometer data from the JSON structure
def extract_acc_data(json_data):
    # Lists to store the acceleration data
    xAcc = []
    yAcc = []
    zAcc = []

    # Iterate through each entry in the JSON data
    for entry in json_data['data']:
        acc_data = entry['acc']
        timestamp = acc_data['Timestamp']  # Extract the timestamp
        timestamps.append(timestamp)  # Store the timestamp

        # Extract x, y, z values from ArrayAcc
        for acc_entry in acc_data['ArrayAcc']:
            xAcc.append(acc_entry['x'])
            yAcc.append(acc_entry['y'])
            zAcc.append(acc_entry['z'])

    return timestamps, xAcc, yAcc, zAcc


# Function to read the .json file
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Right Arm Acc File
file_path = 'right_arm_acc.json' 
json_data = read_json_file(file_path)

# Extract the accelerometer data from the file
timestamps, xAcc, yAcc, zAcc = extract_acc_data(json_data)

# Output the results
print("Timestamps:", timestamps)
print("xAcc:", xAcc)
print("yAcc:", yAcc)
print("zAcc:", zAcc)


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
