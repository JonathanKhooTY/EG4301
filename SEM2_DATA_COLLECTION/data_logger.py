import serial
import csv

arduino_port = "/dev/cu.usbmodem11101"
baud = 115200
fileName = "data.csv"
sensor_data = []
header = ['sensor1','sensor2','button1','button2']
with open(fileName,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

ser = serial.Serial(arduino_port,baud)
print("Connected to arduino port: " + arduino_port)
#file = open(fileName,"a")
#print("created file")

#Data Display


while (True):
    getData = ser.readline()
    dataString = getData.decode('utf-8')
    parsedData = dataString[0:][:-2]
    reading = parsedData.split(",")
    #sensor_data.append(reading)
    print(reading)

    
    with open(fileName,'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(reading)
    
    