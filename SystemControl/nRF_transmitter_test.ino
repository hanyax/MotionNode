#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
Adafruit_BNO055 bno = Adafruit_BNO055(55);

RF24 radio(7, 8);
const int unit = 1;

const byte rxAddr[] = {00001, 00011};

int count = 0;

void setup()
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  radio.begin();
  radio.setRetries(15, 15);
  radio.openWritingPipe(rxAddr[unit]);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  bno.setExtCrystalUse(true);
}

void loop()
{
  sensors_event_t orientationData , angVelocityData , accelerationData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&accelerationData, Adafruit_BNO055::VECTOR_ACCELEROMETER);

  float data[9];
  data[1] = orientationData.orientation.x;
  data[2] = orientationData.orientation.y;
  data[3] = orientationData.orientation.z;
  data[4] = accelerationData.acceleration.x;
  data[5] = accelerationData.acceleration.y;
  data[6] = accelerationData.acceleration.z;
  data[7] = angVelocityData.gyro.x;
  data[8] = angVelocityData.gyro.y;
  data[9] = angVelocityData.gyro.z;
  //, &accelerationData, &angVelocityData);

  radio.write(&data, sizeof(data));


  delay(10);
  Serial.print("X:");
  Serial.print(data[1]);
  Serial.print(", Y:");
  Serial.print(data[2]);
  Serial.print(", Z:");
  Serial.print(data[3]);
  Serial.print("\t");
  Serial.print("Xa:");
  Serial.print(data[4]);
  Serial.print(", Ya:");
  Serial.print(data[5]);
  Serial.print(", Za:");
  Serial.print(data[6]);
  Serial.print("\t");
  Serial.print("Xv:");
  Serial.print(data[7]);
  Serial.print(", Yv:");
  Serial.print(data[8]);
  Serial.print(", Zv:");
  Serial.print(data[9]);
  Serial.print("\t");
  Serial.println("");
}
