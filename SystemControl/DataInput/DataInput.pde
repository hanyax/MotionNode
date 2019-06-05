import processing.serial.*;
Serial mySerial;
PrintWriter output1;
PrintWriter output2;
void setup() {
  mySerial = new Serial( this, Serial.list()[6], 115200 );
  output1 = createWriter( "data.txt" ); 
  output2 = createWriter( "mod2.txt");
  mySerial.readString();
}
void draw() {
  if (mySerial.available() > 0 ) {
    String value = mySerial.readString();        
    output1.print(value);
    print(value);
  }
  delay(1);
} 

void keyPressed() {
  output1.flush();  // Writes the remaining data to the file
  output1.close();  // Finishes the file
  output2.flush();  // Writes the remaining data to the file
  output2.close();  // Finishes the file
  exit();  // Stops the program
}
