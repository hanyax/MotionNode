#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);

typedef enum {
  Idle,
  Down,
  Up,
} states;

int count;
int bad_count;
int down_threhold = 70;
int up_threhold = 40;
int idle_threhold = 70;
states cur_state;

float prev_data1;
float prev_data2;

boolean EnterLow;

const byte rxAddr[] = {00001, 00011};

void setup()
{
  cur_state = Idle;
  count = 0;
  bad_count = 0;
  prev_data1 = 90;
  prev_data2 = 90;
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

  RecieveData(data, pipeNum);
  state_contoller(data);
  Serial.println(cur_state);
  Serial.println(count);
  Serial.println(bad_count);
}

void RecieveData(float* data, byte pipeNum) {
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

void state_contoller(float* data) {
  float cur_data = (prev_data1 + prev_data2 + data[3])/3;
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
  prev_data1 = data[3]; 
}
