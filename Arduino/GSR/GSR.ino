#include <Wire.h>

void setup() {
    Wire.begin(5);
    Wire.onRequest(req_handler);
}

void loop() {
}

void req_handler(){
    Wire.write("%f\n", analogRead(A0));
}
