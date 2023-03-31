#include <Wire.h>

const int GSR=A0;
int sensorValue=0;
int gsr_av=0;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(5);
  Wire.onRequest(req_handler);
}

void req_handler(){
  long sum=0;
  for(int i=0; i<10; i++){
    sum += analogRead(GSR);
    delay(5);
  }
  gsr_av = sum/10;
  Wire.write("%f\n", gsr_av);
}
void loop() {
  // put your main code here, to run repeatedly:
  //long sum=0;
  //for(int i=0; i<10;i++){
  //  sensorValue = analogRead(GSR);
  //  sum += sensorValue;
  //  delay(5);
  //}
  //gsr_av = sum/10;
  //Serial.println(gsr_av);
}
