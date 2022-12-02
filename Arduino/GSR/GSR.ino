#include <Wire.h>

void setup() {
    Wire.begin(5);
    Wire.onRequest(req_handler);
}

void loop() {
}

void req_handler(){
    float sensorval = analogRead(A0);
    Wire.write("%f\n", sensorval);
}
