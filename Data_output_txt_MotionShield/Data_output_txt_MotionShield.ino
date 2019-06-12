#include "NAxisMotion.h"        //Contains the bridge code between the API and the Arduino Environment
#include <Wire.h>

NAxisMotion mySensor;         //Object that for the sensor 
unsigned long lastStreamTime = 0;     //To store the last streamed time stamp
const int streamPeriod = 100;          //To stream at 50Hz without using additional timers (time period(ms) =1000/frequency(Hz))

typedef enum {
  Idle,
  Down,
  Up,
} states;

int count;
int bad_count;
int down_threhold = 70;
int up_threhold = 30;
int idle_threhold = 70;

float prev_data1;
float prev_data2;

boolean EnterLow;

states cur_state;

void setup() //This code is executed once
{    
  cur_state = Idle;
  count = 0;
  bad_count = 0;
  prev_data1 = 90;
  prev_data2 = 90;
  EnterLow = false;
  
  //Peripheral Initialization
  Serial.begin(115200);           //Initialize the Serial Port to view information on the Serial Monitor
  I2C.begin();                    //Initialize I2C communication to the let the library communicate with the sensor.
  //Sensor Initialization
  mySensor.initSensor();          //The I2C Address can be changed here inside this function in the library
  mySensor.setOperationMode(OPERATION_MODE_NDOF);   //Can be configured to other operation modes as desired
  mySensor.setUpdateMode(MANUAL);  //The default is AUTO. Changing to MANUAL requires calling the relevant update functions prior to calling the read functions
  //Setting to MANUAL requires fewer reads to the sensor  
}

void loop() //This code is looped forever
{
  if ((millis() - lastStreamTime) >= streamPeriod)
  {
    lastStreamTime = millis();    
    mySensor.updateEuler();        //Update the Euler data into the structure of the object
    mySensor.updateAccel();        //Update the Accelerometer data
    mySensor.updateCalibStatus();  //Update the Calibration Status

    Serial.print(" H: ");
    Serial.print(mySensor.readEulerHeading()); //Heading data
    Serial.print("deg ");

    Serial.print(" R: ");
    Serial.print(mySensor.readEulerRoll()); //Roll data
    Serial.print("deg");

    Serial.print(" P: ");
    Serial.print(mySensor.readEulerPitch()); //Pitch data
    Serial.print("deg ");

    Serial.print(" aX: ");
    Serial.print(mySensor.readAccelX()); //Accelerometer X-Axis data
    Serial.print("m/s2 ");

    Serial.print(" aY: ");
    Serial.print(mySensor.readAccelY());  //Accelerometer Y-Axis data
    Serial.print("m/s2 ");

    Serial.print(" aZ: ");
    Serial.print(mySensor.readAccelZ());  //Accelerometer Z-Axis data
    Serial.print("m/s2 ");

    Serial.println();
    
    float data = mySensor.readEulerPitch();
    state_contoller(data);
    //Serial.println(cur_state);
    //Serial.println(count);
    //Serial.println(bad_count);
  }
}


void state_contoller(float data) {
  float cur_data = (prev_data1 + prev_data2 + data)/3;
  if (cur_state == Idle) {
    if (data < down_threhold) {  // switch to down mode
      cur_state = Down;
      count++;
    } else {
      cur_state = cur_state;
    }
  } else if (cur_state == Down) {
    if (data < up_threhold) {  // switch to up mode
      if (EnterLow == false) {
        EnterLow = true;
      } 
    } else if (data > up_threhold) {
      if (EnterLow == true) {
        cur_state = Up; 
      } 
      EnterLow = false;
    } else {
      cur_state = cur_state;
    }
  } else if (cur_state == Up) {
    if (data > idle_threhold) {  // switch to up mode
      cur_state = Idle;
    } else {
      cur_state = cur_state;
    }
  } else {
    cur_state = cur_state;
  }

  // update previous data
  prev_data2 = prev_data1;
  prev_data1 = data; 
}
