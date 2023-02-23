
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import csv
from datetime import datetime

arduino_port = '/dev/cu.usbmodem1101'
baud = 9600
sensors = [['LU','MU','RU'],
['LM','MM','RM'],
['LB','MB','RB']]

header = ['Date/Time','LU','MU','RU','LM','MM','RM','LB','MB','RB'] #For CSV file
fileName = "pressure_data.csv"

# Set up serial communication with Arduino
ser = serial.Serial(arduino_port,baud)  
ser.flushInput()

with open(fileName,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Set up plot
fig, ax = plt.subplots(3, 3, figsize=(20, 15))
lines = []
for i in range(3):
    for j in range(3):
        line, = ax[i, j].plot([], [])
        lines.append(line)
        ax[i, j].set_xlim(0, 60)  #Desired x-axis limit
        ax[i, j].set_ylim(0, 800)  # Max value of your sensor
        ax[i, j].set_title(sensors[i][j])
        ax[i, j].grid('true','both')
        #ax[i, j].set_title(f"Sensor {i*3+j+1}")



# Define function to update plot
def update_plot(frame):
    try:
        data = ser.readline().decode().rstrip().split(',')
    
        currentTime = str(datetime.now())
        

        if len(data) == 9:
            data = [int(x) for x in data]
            for i, line in enumerate(lines):
                line.set_data(np.arange(len(line.get_xdata())+1), np.append(line.get_ydata(), data[i]))
                if len(line.get_xdata()) > 60:
                    line.set_xdata(line.get_xdata()[1:])
                    line.set_ydata(line.get_ydata()[1:])
                    ax[i//3, i%3].set_xlim(line.get_xdata()[0], line.get_xdata()[-1])

        data.insert(0,currentTime)
        print(data) #DEBUG
        with open(fileName,'a', encoding='UTF8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    except KeyboardInterrupt:
        print("Plot closed.")
        if ani.event_source is not None:
            ani.event_source.stop()  # stop the animation before closing the plot window    
        plt.close()
    return lines

# Animate plot
ani = animation.FuncAnimation(fig, update_plot, blit=True)


plt.show()
