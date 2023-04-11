import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


arduino_port = '/dev/cu.usbmodem1101'
baud = 115200


# Set up serial communication with Arduino
ser = serial.Serial(arduino_port,baud)  
ser.flushInput()

# Define pressure matrix size
rows = 3
cols = 3

# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, cols-1)
ax.set_ylim(0, rows-1)
ax.invert_yaxis()
ax.grid('both')
# Create scatter plot for centroid coordinates
scatter = ax.scatter([], [])

# Define function to update scatter plot
def update(i):

    # Remove existing text labels
    for text in ax.texts:
        text.remove()
        
    # Read serial data
    data = ser.readline().decode().rstrip().split(',')
    matpressureData = data[0:9]
    #matpressureData = [(float(x) - 21.0) if float(x) >= 21 else 0 for x in matpressureData]  #Correction for the non-zero start state

    if len(matpressureData) != rows*cols:
        return scatter,

    # Convert data to pressure matrix
    pressure = np.array(matpressureData,dtype=float).reshape(rows, cols)
    #print(pressure)
    # Calculate total pressure
    total_pressure = np.sum(pressure)

    # Calculate weighted average
    weighted_row = np.sum(np.sum(pressure, axis=1) * np.arange(rows))
    weighted_col = np.sum(np.sum(pressure, axis=0) * np.arange(cols))
    if total_pressure == 0:
        centroid_row = 1.0
        centroid_col = 1.0
        
    else:
        centroid_row = weighted_row / total_pressure
        centroid_col = weighted_col / total_pressure
        
    print("Centroid coordinates: ({:.3f}, {:.3f})\n".format(centroid_col, centroid_row))
    # Update scatter plot
    scatter.set_offsets([(centroid_col, centroid_row)])
    # Add total pressure label
    ax.text(centroid_col+0.1, centroid_row+0.1, 'Total Pressure: {:.3f}'.format(total_pressure-189))
    ax.text(centroid_col+0.1, centroid_row+0.2, 'Coordinates: {:.3f}'.format(centroid_col))
    ax.text(centroid_col+0.7, centroid_row+0.2, '{:.3f}'.format(centroid_row))
    

    return scatter,

# Create animation
ani = animation.FuncAnimation(fig, update, interval=1000)

# Show plot
plt.show()

# Close serial communication
ser.close()