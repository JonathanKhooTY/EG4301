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

unsigned long last_time;
int interval = 500;
double Kp = 100;
double set_pressure = 105;
double control_signal;

const int INF = 11;
const int DEF = 4;
void setup() {
  // Initalize UART, I2C bus, and connect to the micropressure sensor
  Serial.begin(115200);
  Wire.begin();
  pinMode(INF,OUTPUT);
  pinMode(DEF,OUTPUT);

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
  //Serial.print(mpr.readPressure(),4);
  //Serial.println(" PSI");
  //Serial.print(mpr.readPressure(PA),1);
  //Serial.println(" Pa");
  //Serial.print(mpr.readPressure(KPA),4);
  //Serial.println(" kPa");
  /*
  double currentPressure = mpr.readPressure(KPA);
  Serial.print(currentPressure);
  Serial.println(" KPa");
  /*
  Serial.print(mpr.readPressure(TORR),3);
  Serial.println(" torr");
  Serial.print(mpr.readPressure(INHG),4);
  Serial.println(" inHg");
  Serial.print(mpr.readPressure(ATM),6);
  Serial.println(" atm");
  Serial.print(mpr.readPressure(BAR),6);
  Serial.println(" bar");
  
  */
  /*
  Serial.println();
  delay(1000);


  if (currentPressure < 105){
    Serial.println("Pressure below threshold, motor activated");
  } 
  */

  PID_Control();
}

void PID_Control(){

  unsigned long current_time = millis();
  int delta_time = current_time - last_time;

  if (delta_time >= interval){
    
    double currentPressure = mpr.readPressure(KPA);
    Serial.print(currentPressure);  //Internal pressure in kpa
    Serial.print(",");
    //Serial.println(" KPa");
    //Serial.println();

    double error = set_pressure - currentPressure; //+ve error means current pressure is low, -ve error means current pressure is high
    
    //Serial.println(" error");
    //Serial.println();
    if (error > 0){
      double control_signal = Kp * error;
      Serial.print(error);  // raw error value
      Serial.print(",");
      Serial.println(control_signal);  //applied control signal before PWM modulation
    //Serial.print(",");
    //Serial.println(" control signal");
    //Serial.println();

      int pwm = control_signal;
      digitalWrite(DEF,LOW);
      analogWrite(INF,pwm);
      //digitalWrite(DEF,LOW);

    } else if (error < 0){
      //int control_signal = Kp * abs(error);
      Serial.print(error);  // raw error value
      Serial.print(",");
      Serial.println(-1); //control signal
      digitalWrite(DEF,HIGH);
      analogWrite(INF,0);
      
    }
    else {
      Serial.print(error);
      Serial.print(",");
      Serial.println(0);
      analogWrite(INF,0);
      digitalWrite(DEF,LOW);
      
      

    }
    
    last_time = current_time;

  }

}