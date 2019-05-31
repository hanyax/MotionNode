#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);

const byte rxAddr[] = {00001, 00011};

void setup()
{
  while (!Serial);
  Serial.begin(115200);
  //Serial.println("startup!!!");
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
    String dataSend = String(pipeNum);
    dataSend += " H: " + String(data[1]) + "deg ";
    dataSend += " R: " + String(data[2]) + "deg ";
    dataSend += " P: " + String(data[3]) + "deg ";

    dataSend += " aX: " + String(data[4]) + "m/s2 ";
    dataSend += " aY: " + String(data[5]) + "m/s2 ";
    dataSend += " aZ: " + String(data[6]) + "m/s2 ";

    Serial.println(dataSend);
    delay(5);
  }
}
