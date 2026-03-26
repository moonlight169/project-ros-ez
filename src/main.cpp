#include <Arduino.h>
#include <HardwareSerial.h>

// === PIN CONFIG ===
const int vr      = 32;
const int relay   = 23;
const int PIN_FWD = 15;
const int PIN_REV = 22;
const int PIN_ALL = 4;

const int TX_PINS[4] = {13, 27, 26, 25};

HardwareSerial SlaveSerial(1);

struct SlaveCommand {
  int   wheel;
  int   timer;
  float kp, ki, kd;
  int   rpm_in;
};

void sendToSlave(int idx, SlaveCommand cmd) {
  SlaveSerial.end();
  SlaveSerial.begin(9600, SERIAL_8N1, -1, TX_PINS[idx]);

  char buf[64];
  snprintf(buf, sizeof(buf), "[%d,%d,%.1f,%.1f,%.1f,%d]\n",
           cmd.wheel, cmd.timer,
           cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);

  digitalWrite(PIN_ALL, HIGH);
  SlaveSerial.print(buf);
  SlaveSerial.flush();
  digitalWrite(PIN_ALL, LOW);

  Serial.printf("[TX→S%d] %s", idx + 1, buf);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_FWD, OUTPUT);
  pinMode(PIN_REV, OUTPUT);
  pinMode(PIN_ALL, OUTPUT);
  pinMode(relay,   OUTPUT);
  digitalWrite(PIN_ALL, LOW);
  digitalWrite(relay,   HIGH);
  Serial.println("Master ready");
}

void loop() {
  int val    = analogRead(vr);
  int mapval = map(val, 0, 4095, 0, 100);

  // relay + direction
  if (mapval > 50) {
    digitalWrite(PIN_FWD, HIGH);
    digitalWrite(PIN_REV, LOW);
    digitalWrite(relay,   HIGH);
  } else {
    digitalWrite(PIN_FWD, LOW);
    digitalWrite(PIN_REV, HIGH);
    digitalWrite(relay,   LOW);
  }

  // ส่งไป Slave ทีละตัว
  for (int i = 0; i < 4; i++) {
    SlaveCommand cmd = {
      i + 1,   // wheel 1-4
      160,     // timer
      1.0,     // kp
      1.0,     // ki
      1.0,     // kd
      mapval * 5 // rpm_in (0-500)
    };
    sendToSlave(i, cmd);
    delay(20);
  }

  delay(500);
}