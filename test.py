import pandas as pd

# Sample code to read data from a CSV file
data = pd.read_json('20240902T084552Z_233830000605_acc_stream.json')

# Assume the CSV file has columns named 'X', 'Y', and 'Z'
x = data['X']
y = data['Y']
z = data['Z']

import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

# Create a new figure
fig = plt.figure()

# Add a 3D subplot
ax = fig.add_subplot(111, projection='3d')

# Plot the data
ax.scatter(x, y, z)

# Add labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Add a title
ax.set_title('3D Scatter Plot')

# Show the plot
plt.show()

# Ella test to add
ax.set_title('ella test new')
