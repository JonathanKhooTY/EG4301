import serial
import csv
from datetime import datetime
import numpy as np
import threading #To allow for code to run while waiting for an hour
import pandas as pd
import time

fileTime = str(datetime.now().strftime('%H-%M-%S'))
arduino_port = "/dev/cu.usbmodem1101"
baud = 115200
fileName = f"data_log_{fileTime}.csv"

sensor_data = []
# Define pressure matrix size
rows = 3
cols = 3
#length = 0
global mean_raw_sum, std_raw_sum, mean_x_coord, std_x_coord, mean_y_coord, std_y_coord, thresholdObtained,fileName_ICM

icmcounter_raw_sum = 0
icmcounter_x_coord = 0
icmcounter_y_coord = 0

thresholdObtained = False


header = ['Date/Time','LL','ML','RL','LU','MU','RU','LB','MB','RB','AIR_RB','AIR_LU','AIR_LL','AIR_RL','AIR_RU','AIR_LB','RAW_SUM','X_COORD','Y_COORD']
with open(fileName,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)



ser = serial.Serial(arduino_port,baud)
print("Connected to arduino port: " + arduino_port)
#file = open(fileName,"a")
#print("created file")

def threshold_identify():
    global mean_raw_sum, std_raw_sum, mean_x_coord, std_x_coord, mean_y_coord, std_y_coord, thresholdObtained, fileName_ICM
    header = ['Time','Raw Sum','X Coord','Y Coord']
    fileTime = str(datetime.now().strftime('%H-%M-%S'))
    fileName_ICM = f"data_log_ICM_{fileTime}.csv"           #Note diff file name for ICM instances recording
    with open(fileName_ICM,'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    data = pd.read_csv(fileName)                        #Note this is fileName, NOT fileName_ICM
    icm_raw_sum = data['RAW_SUM'].values
    icm_x_coord = data['X_COORD'].values
    icm_y_coord = data['Y_COORD'].values

    icm_value_length = len(icm_raw_sum)

    mean_raw_sum = np.mean(icm_raw_sum)
    std_raw_sum = np.std(icm_raw_sum)

    mean_x_coord = np.mean(icm_x_coord)
    std_x_coord = np.std(icm_x_coord)

    mean_y_coord = np.mean(icm_y_coord)
    std_y_coord = np.std(icm_y_coord)

    thresholdObtained = True
    
    
    #print(f': {}')
    #return mean_raw_sum,mean_x_coord,mean_y_coord,std_raw_sum,std_x_coord,std_y_coord




def icm_identify(data): #Data format: [RAW SUM PRESSURE, X COORD, Y COORD] AI needs total # of detected ICMs in a 10 minute window
    global mean_raw_sum, std_raw_sum, mean_x_coord, std_x_coord, mean_y_coord, std_y_coord,icmcounter_raw_sum,icmcounter_x_coord,icmcounter_y_coord

    raw_sum = data[0]
    x_coord = data[1]
    y_coord = data[2]


    raw_sum_Zscore = abs((raw_sum - mean_raw_sum) / std_raw_sum)
    x_coord_Zscore = abs((x_coord - mean_x_coord) / std_x_coord)
    y_coord_Zscore = abs((y_coord - mean_y_coord) / std_y_coord)

    if raw_sum_Zscore > 2:
         icmcounter_raw_sum += 1

    if x_coord_Zscore > 2:
         icmcounter_x_coord += 1
    if y_coord_Zscore > 2:
         icmcounter_y_coord += 1
    
    return [icmcounter_raw_sum,icmcounter_x_coord,icmcounter_y_coord]
    
    #print(f'{mean_raw_sum,std_x_coord,std_y_coord}')
    #print(f'ZSCORES: {raw_sum_Zscore}, {x_coord_Zscore}, {y_coord_Zscore}')



def write_to_file(data):
    
    fileTime = str(datetime.now().strftime('%H-%M-%S'))
    data.insert(0,fileTime)
    # open file and write value
    with open(fileName_ICM,'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    print(f'Written {data}')




threading.Timer(31, threshold_identify).start()#Remember to x+1 after desired time cos timer starts exactly at T=x TO BE SET TO AN HOUR
starting_time = time.time() #For ICM csv file updating 
while (True):
    data = ser.readline().decode().rstrip().split(',')
    airpressureData = data[9:]
    matpressureData = data[0:9]
    #print(airpressureData)
    #print(matpressureData)
    currentTime = str(datetime.now().strftime('%H:%M:%S'))
    data.insert(0,currentTime)

    # Centroid calculation
    # Convert data to pressure matrix
    pressure = np.array(matpressureData,dtype=float).reshape(rows, cols)
    #print(pressure)
    # Calculate total pressure
    total_pressure = np.sum(pressure)

    # Calculate weighted average
    weighted_row = np.sum(np.sum(pressure, axis=1) * np.arange(rows))
    weighted_col = np.sum(np.sum(pressure, axis=0) * np.arange(cols))
    centroid_row = weighted_row / total_pressure
    centroid_col = weighted_col / total_pressure
    #print("Centroid coordinates: ({:.3f}, {:.3f})\n".format(centroid_col, centroid_row))
    #rawSum = sum(map(float, matpressureData))
    data.insert(16,total_pressure)
    data.insert(17,centroid_col)
    data.insert(18,centroid_row)
    icm_data = [total_pressure,centroid_col,centroid_row]
    print(icm_data)
    

    with open(fileName,'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
    
    if thresholdObtained:
        #print(f'THRESHOLD OBTAINED: {mean_raw_sum,mean_x_coord,mean_y_coord,std_raw_sum,std_x_coord,std_y_coord}')
        time_interval = 11 #Update icm csv file every 10 minutes
        
        identified_icm = icm_identify(icm_data)
        if time.time() - starting_time >= time_interval:
            write_to_file(identified_icm)
            icmcounter_raw_sum = 0
            icmcounter_x_coord = 0
            icmcounter_y_coord = 0

            starting_time = time.time()

        print(f'{identified_icm}')