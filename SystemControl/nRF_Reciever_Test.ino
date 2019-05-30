#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);

const byte rxAddr[] = {00001, 00011};

void setup()
{
  while (!Serial);
  Serial.begin(115200);
  Serial.println("startup!!!");
  radio.begin();
  //Serial.println("radio!!!");
  radio.openReadingPipe(1, rxAddr[1]);
  //Serial.println("reading!!!");
  radio.openReadingPipe(2, rxAddr[2]);
  //Serial.println("reading2!!!");
  radio.startListening();
  //Serial.println("listen!!!");
}

void loop()
{
  delay(2);
  char text[32] = {0};
  float data[9];
  byte pipeNum = 0; //variable to hold which reading pipe sent data

  while (radio.available(&pipeNum)) { //Check if received data
    //Serial.println("recieved");
    radio.read(&data, sizeof(data));
    //Serial.print("X");
    Serial.print(" H: ");
    Serial.print(data[1]);
    Serial.print("deg ");
    Serial.print(" R: ");
    Serial.print(data[2]);
    Serial.print("deg ");
    Serial.print(" P: ");
    Serial.print(data[3]);
    Serial.print("deg ");

    Serial.print(" aX: ");
    Serial.print(data[4]);
    Serial.print("m/s2 ");
    Serial.print(" aY: ");
    Serial.print(data[5]);
    Serial.print("m/s2 ");
    Serial.print(" aZ: ");
    Serial.print(data[6]);
    Serial.print("m/s2 ");

    Serial.println("");
    delay(10);
  }
}
