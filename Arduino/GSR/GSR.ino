#include <Wire.h>

void setup() {
    Wire.begin(8);
    Wire.onRequest(req_handler);
}

void loop() {
}

void req_handler(){
    Wire.write(analogRead(A0));
}
