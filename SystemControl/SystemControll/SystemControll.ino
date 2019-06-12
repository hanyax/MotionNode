#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);

const byte rxAddr[] = {00001, 00011};

typedef enum {
  Idle,
  Down,
  Up,
} states;

int count;
int bad_count;
int down_threhold = 50;
int up_threhold = 45;
int idle_threhold = 50;

boolean EnterLow;
boolean minPcounted;
boolean maxPcounted;

int minDown_threhold = -10;
int maxDown_threhold = 15;

static int min_P_Value = 80;
static int reg_P_Value = 80;
int minP;

states cur_state;


void setup()
{
  cur_state = Idle;
  count = 0;
  bad_count = 0;
  minP = min_P_Value;
  EnterLow = false;
  
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

void loop() {
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
    
    state_contoller(data[3]);
    Serial.println(dataSend);
    Serial.println(cur_state);
    Serial.println(count);
    Serial.println(bad_count);
    Serial.println();
    
    delay(10);
  }
}

void state_contoller(float data) {  
  if (cur_state == Idle) {
    minP = min_P_Value;
    minPcounted = false;
    maxPcounted = false;
    if (data < down_threhold) {  // switch to down mode
      cur_state = Down;
      count++;
    } 
  } else if (cur_state == Down) {
    if (data < up_threhold) {  // switch to up mode
      if (EnterLow == false) {
        EnterLow = true;
      } 
    } else if (data > up_threhold) {
      if (EnterLow == true) {
        cur_state = Up; 
        EnterLow = false;
        if (minP > maxDown_threhold && maxPcounted == false) {
          bad_count++;
          maxPcounted = true;
        }
      }
    } else {
      cur_state = cur_state;
    }
    if (data < minP) {
      minP = data;
    }
  } else if (cur_state == Up) {

    // check lowest bent point
    if (minP < minDown_threhold && minPcounted == false) {
      bad_count++;
      minPcounted = true;
    }
    
    if (data > idle_threhold) {  // switch to up mode
      cur_state = Idle;
    } else {
      cur_state = cur_state;
    }
  } else {
    cur_state = cur_state;
  }

}
