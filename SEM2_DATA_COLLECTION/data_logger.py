import serial
import csv
from datetime import datetime

arduino_port = "/dev/cu.usbmodem1101"
baud = 115200
fileName = "data.csv"
sensor_data = []
header = ['Date/Time','LL','ML','RL','LU','MU','RU','LB','MB','RB','AIR_RB','AIR_LU','AIR_LL','AIR_RL','AIR_RU','AIR_LB']
with open(fileName,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

ser = serial.Serial(arduino_port,baud)
print("Connected to arduino port: " + arduino_port)
#file = open(fileName,"a")
#print("created file")

#Data Display


while (True):
    data = ser.readline().decode().rstrip().split(',')
    airpressureData = data[9:]
    matpressureData = data[0:9]
    #print(airpressureData)
    #print(matpressureData)
    currentTime = str(datetime.now().strftime('%H:%M:%S'))
    data.insert(0,currentTime)
    print(airpressureData)
    print(matpressureData)

    with open(fileName,'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    