import serial
import csv

arduino_port = "/dev/cu.usbmodem1101"
baud = 115200
fileName = "data.csv"
sensor_data = []
header = ['sensor0_NOSENSORATTACHED','LowerLeft','UpperLeft','UpperRight','LeftButt','RightButt','Config_1_B0','Config_2_B1','Config_3_B2','Butt_Inflate_B3','Buff_Deflate_B4','Upper_Inflate_B5'
,'Upper_Deflate_B6','Lower_Inflate_B7','Lower_Deflate_B8']
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
    
    