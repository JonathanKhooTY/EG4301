const int numRows = 3;  // number of rows in the matrix
const int numCols = 2;  // number of columns in the matrix

int sensorPins[numRows][numCols] = {  // 2D array of sensor pins
  {A0, A1},
  {A2, A3},
  {A4, A5}
};

int sensorValues[numRows][numCols];  // 2D array of sensor values

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);
}

void loop() {
  // read sensor values
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      sensorValues[row][col] = analogRead(sensorPins[row][col]);
    }
  }
  
  // print sensor values to serial monitor
  for (int row = 0; row < numRows; row++) {
    for (int col = 0; col < numCols; col++) {
      Serial.print(sensorValues[row][col]);
      Serial.print(",");
    }
    //Serial.println();
  }
  Serial.println("");
  // delay before next reading
  delay(1000);
}