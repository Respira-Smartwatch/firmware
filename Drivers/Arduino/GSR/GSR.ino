#include <Wire.h>

int led = 13;

void setup() {
    Wire.begin(0x08);
    Wire.onRequest(req_handler);
    pinMode(led, OUTPUT);
    digitalWrite(led, HIGH);
    delay(1000);
    digitalWrite(led, LOW);
}

void loop() {
}

void req_handler(){
    digitalWrite(led, HIGH);
    Wire.write(analogRead(A0));
    digitalWrite(led, LOW);
}
