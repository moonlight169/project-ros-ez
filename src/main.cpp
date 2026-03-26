#include <Arduino.h>

int vr = 32;
int val = 0;
int keera = 0;
int relay = 23;

void setup(){
  Serial.begin(115200);
  pinMode(15, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, 1);

}

void loop(){
  val = analogRead(vr);
  long mapval = map(val, 0, 4095, 0, 100);
  if (mapval > 50){
    digitalWrite(15, 1);
    digitalWrite(22, 0);
    keera = 1;
  } else {
    digitalWrite(22, 1);
    digitalWrite(15, 0);
    keera = 0;
  }
  if (keera == 1){
    digitalWrite(relay, 1);
  }
  else {
    digitalWrite(relay, 0);
  }

}