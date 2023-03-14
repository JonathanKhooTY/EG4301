import serial
import csv
from datetime import datetime

arduino_port = "/dev/cu.usbmodem1101"
baud = 115200
fileName = "data.csv"
sensor_data = []
header = ['Date/Time','Right_Butt','Left_Upper','Left_Lower','Right_Lower','Right_Upper','Left_Butt']
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
    #matpressureData = data[0:9]
    #print(airpressureData)
    #print(matpressureData)
    currentTime = str(datetime.now())
    airpressureData.insert(0,currentTime)
    print(airpressureData)

    with open(fileName,'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(airpressureData)
    
    