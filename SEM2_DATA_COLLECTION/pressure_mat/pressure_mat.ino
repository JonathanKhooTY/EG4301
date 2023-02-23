const int numRows = 3;  // number of rows in the matrix
const int numCols = 3;  // number of columns in the matrix

int sensorPins[numCols] = {A2, A1, A0};

int digitalPins[numCols] = {10,8,6};


int sensorValues[numRows][numCols];  // 2D array of sensor values

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);

  pinMode(6, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  }

void loop() {
  
  for (int n = 0; n < numCols; n++){
    digitalWrite(digitalPins[n],LOW); //CALIBRATE ALL AS LOW FIRST
  }

  // read sensor values
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      digitalWrite(digitalPins[col],HIGH);    //SET TO HIGH WHEN READING
      sensorValues[row][col] = analogRead(sensorPins[row]);
      digitalWrite(digitalPins[col],LOW);     //RESET TO LOW AFTER READING
    }
  }
  
  // print sensor values to serial monitor
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      Serial.print(sensorValues[row][col]);
      if (row == 2 && col == 2) continue;
      Serial.print(",");
    }
    //Serial.println();
  }
  Serial.println("");
  // delay before next reading
  delay(1000);
}