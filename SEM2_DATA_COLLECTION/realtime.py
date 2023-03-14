
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import csv
from datetime import datetime

arduino_port = '/dev/cu.usbmodem1101'
baud = 115200
sensors = [['LU','MU','RU'],
['LM','MM','RM'],
['LB','MB','RB']]

fileTime = datetime.now().strftime('%H-%M-%S')
header = ['Date/Time','LL','ML','RL','LU','MU','RU','LB','MB','RB',] #For CSV file
fileName = f"pressure_data_{fileTime}.csv"

# Set up serial communication with Arduino
ser = serial.Serial(arduino_port,baud)  
ser.flushInput()

with open(fileName,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)



# Set up plot
fig, ax = plt.subplots(3, 3, figsize=(20, 15))
major_ticks = np.arange(0, 1001, 100)
minor_ticks = np.arange(0, 1001, 50)

lines = []
for i in range(3):
    for j in range(3):
        line, = ax[i, j].plot([], [])
        lines.append(line)
        ax[i, j].set_xlim(0, 60)  #Desired x-axis limit
        ax[i, j].set_ylim(0, 1023)  # Max value of your sensor
        ax[i, j].set_title(sensors[i][j])
        ax[i, j].grid('both','both')
        #ax[i,j ].set_yticks(range(0,500))
        ax[i,j].set_yticks(minor_ticks, minor=True)
        
        
        #ax[i, j].set_title(f"Sensor {i*3+j+1}")



# Define function to update plot
def update_plot(frame):
    try:
        data = ser.readline().decode().rstrip().split(',')
        airpressureData = data[9:]
        matpressureData = data[0:9]
        print(airpressureData)
        print(matpressureData)
        currentTime = str(datetime.now())
        
        
        if len(matpressureData) == 9:
            matpressureData = [int(x) for x in matpressureData]
            for i, line in enumerate(lines):
                line.set_data(np.arange(len(line.get_xdata())+1), np.append(line.get_ydata(), matpressureData[i]))
                if len(line.get_xdata()) > 60:
                    line.set_xdata(line.get_xdata()[1:])
                    line.set_ydata(line.get_ydata()[1:])
                    ax[i//3, i%3].set_xlim(line.get_xdata()[0], line.get_xdata()[-1])
        
        data.insert(0,currentTime)
        #print(data) #DEBUG
        with open(fileName,'a', encoding='UTF8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
            #
    except KeyboardInterrupt:
        print("Plot closed.")
        if ani.event_source is not None:
            ani.event_source.stop()  # stop the animation before closing the plot window    
        plt.close()
    return lines

# Animate plot
ani = animation.FuncAnimation(fig, update_plot, blit=True)


plt.show()
