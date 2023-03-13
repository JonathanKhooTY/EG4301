#include <SPI.h>
#include<Wire.h>
#include <SparkFun_MicroPressure.h>

SparkFun_MicroPressure mpr;
#define TCAADDR 0x70
const int numRows = 3;  // number of rows in the matrix
const int numCols = 3;  // number of columns in the matrix

int sensorPins[numCols] = {A2, A1, A0};

//int digitalPins[numCols] = {10,8,6};


int digitalPins[numRows][numCols] = {
  {12,11,10},
  {9,8,7},
  {6,5,4}
  };

int sensorValues[numRows][numCols];  // 2D array of sensor values


void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(2);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);

  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);

  tcaselect(0);
  tcaselect(1); //need to initialize this in setup
  tcaselect(2);
  tcaselect(3);
  tcaselect(4);
  tcaselect(5);

  if(!mpr.begin())
  {
    Serial.println("Cannot connect to MicroPressure sensor.");
    while(1);
  }
  
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      digitalWrite(digitalPins[row][col],LOW);    //SET TO HIGH WHEN READING
    }
  }
  
}

void loop() {


  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      digitalWrite(digitalPins[row][col],HIGH);   //SET TO HIGH WHEN READING
      sensorValues[row][col] = analogRead(sensorPins[row]);
      digitalWrite(digitalPins[row][col],LOW);    
      delay(2); //RESET TO LOW AFTER READING
    }
  }
  

  /*
  // read sensor values
  //for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      digitalWrite(digitalPins[col],HIGH);   //SET TO HIGH WHEN READING
      sensorValues[0][col] = analogRead(sensorPins[0]);
      sensorValues[1][col] = analogRead(sensorPins[1]);
      sensorValues[2][col] = analogRead(sensorPins[2]);
      delay(2);
      digitalWrite(digitalPins[col],LOW);    
      delay(2); //RESET TO LOW AFTER READING
    }
 // }
  */
  // print sensor values to serial monitor
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      Serial.print(sensorValues[row][col]);
      if (row == 2 && col == 2) continue;
      Serial.print(","); 
    }
    //Serial.println(); 
  }


  Serial.print(",");
  tcaselect(0);
  Serial.print(mpr.readPressure(PA));
  Serial.print(",");
  tcaselect(1);
  //Serial.print("SD1 sensor reading: ");
  Serial.print(mpr.readPressure(PA));
  Serial.print(",");
  //Serial.println();
  //delay(500);
  tcaselect(2);
  //Serial.print("SD2 sensor reading: ");
  Serial.print(mpr.readPressure(PA));
  Serial.print(",");

  tcaselect(3);
  Serial.print(mpr.readPressure(PA));
  Serial.print(",");

  tcaselect(4);
  Serial.print(mpr.readPressure(PA));
  Serial.print(",");

  tcaselect(5);
  Serial.print(mpr.readPressure(PA));
  Serial.println("");
  // delay before next reading
  
  
  delay(1000); //time interval for measurements
  
}