
#include<Wire.h>
#include <SparkFun_MicroPressure.h>

/*
 * Initialize Constructor
 * Optional parameters:
 *  - EOC_PIN: End Of Conversion (defualt: -1)
 *  - RST_PIN: Reset (defualt: -1)
 *  - MIN_PSI: Minimum Pressure (default: 0 PSI)
 *  - MAX_PSI: Maximum Pressure (default: 25 PSI)
 */
//SparkFun_MicroPressure mpr(EOC_PIN, RST_PIN, MIN_PSI, MAX_PSI);
SparkFun_MicroPressure mpr; // Use default values with reset and EOC pins unused
#define TCAADDR 0x70

//Push Button allocations
const int button1 = A0;
const int button2 = A1;

int button1State = 1;
int button2State = 1;


void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup() {

  pinMode(button1, INPUT_PULLUP);
  pinMode(button2,INPUT_PULLUP);
  // Initalize UART, I2C bus, and connect to the micropressure sensor
  Serial.begin(115200);
  Wire.begin();
  //tcaselect(1); //need to initialize this in setup
  //tcaselect(2);
  /* The micropressure sensor uses default settings with the address 0x18 using Wire.

     The mircropressure sensor has a fixed I2C address, if another address is used it
     can be defined here. If you need to use two micropressure sensors, and your
     microcontroller has multiple I2C buses, these parameters can be changed here.

     E.g. mpr.begin(ADDRESS, Wire1)

     Will return true on success or false on failure to communicate. */
  if(!mpr.begin())
  {
    Serial.println("Cannot connect to MicroPressure sensor.");
    while(1);
  }
}

void loop() {

  
  /* The micropressure sensor outputs pressure readings in pounds per square inch (PSI).
     Optionally, if you prefer pressure in another unit, the library can convert the
     pressure reading to: pascals, kilopascals, bar, torr, inches of murcury, and
     atmospheres.
   */
   button1State = digitalRead(button1);
   button2State = digitalRead(button2);
   /*
  if (button1State == LOW){
    Serial.println("B1 pushed");
    //delay(200);
  }
  
  if (button2State == LOW){
    Serial.println("B2 pushed");
    //delay(200);
  }

  */
  tcaselect(1);
  //Serial.print("SD1 sensor reading: ");
  Serial.print(mpr.readPressure(KPA),4);
  Serial.print(",");
  //Serial.println();
  //delay(500);
  tcaselect(2);
  //Serial.print("SD2 sensor reading: ");
  Serial.print(mpr.readPressure(KPA),4);
  Serial.print(",");
  Serial.print(button1State);
  Serial.print(",");
  Serial.println(button2State);
  //Serial.println(" kPa");
  //Serial.println();
  delay(500);
  
}