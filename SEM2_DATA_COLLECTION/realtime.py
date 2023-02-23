import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Set up serial communication with Arduino
ser = serial.Serial('/dev/cu.usbmodem1101', 9600)  # replace 'COM3' with your Arduino's serial port
ser.flushInput()

sensors = [['LU','MU','RU'],
['LM','MM','RM'],
['LB','MB','RB']]

# Set up plot
fig, ax = plt.subplots(3, 3, figsize=(20, 10))
lines = []
for i in range(3):
    for j in range(3):
        line, = ax[i, j].plot([], [])
        lines.append(line)
        ax[i, j].set_xlim(0, 100)  #Desired x-axis limit
        ax[i, j].set_ylim(0, 1023)  # Max value of your sensor
        ax[i, j].set_title(sensors[i][j])
        #ax[i, j].set_title(f"Sensor {i*3+j+1}")

# Define function to update plot
def update_plot(frame):
    data = ser.readline().decode().rstrip().split(',')
    if len(data) == 9:
        data = [int(x) for x in data]
        for i, line in enumerate(lines):
            line.set_data(np.arange(len(line.get_xdata())+1), np.append(line.get_ydata(), data[i]))
            if len(line.get_xdata()) > 100:
                line.set_xdata(line.get_xdata()[1:])
                line.set_ydata(line.get_ydata()[1:])
                ax[i//3, i%3].set_xlim(line.get_xdata()[0], line.get_xdata()[-1])
    return lines

# Animate plot
ani = animation.FuncAnimation(fig, update_plot, blit=True)

plt.show()
