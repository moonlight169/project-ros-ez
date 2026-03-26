#include <Arduino.h>
#include <HardwareSerial.h>

// ==============================
// เปลี่ยนเลขนี้แต่ละตัว: 1,2,3,4
#define MY_WHEEL 1
// ==============================

HardwareSerial fromMaster(1); // RX=16

const int PIN_ENABLE = 4;

struct SlaveCommand {
  int   wheel;
  int   timer;
  float kp, ki, kd;
  int   rpm_in;
};

bool parsePacket(String line, SlaveCommand &cmd) {
  line.replace("[", "");
  line.replace("]", "");

  int idx = 0;
  String t[6];
  for (char c : line) {
    if (c == ',') { idx++; if (idx >= 6) return false; }
    else t[idx] += c;
  }
  if (idx != 5) return false;

  cmd.wheel  = t[0].toInt();
  cmd.timer  = t[1].toInt();
  cmd.kp     = t[2].toFloat();
  cmd.ki     = t[3].toFloat();
  cmd.kd     = t[4].toFloat();
  cmd.rpm_in = t[5].toInt();
  return true;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENABLE, INPUT);
  fromMaster.begin(9600, SERIAL_8N1, 16, -1); // RX=16 only
  Serial.printf("Slave %d ready\n", MY_WHEEL);
}

void loop() {
  if (digitalRead(PIN_ENABLE) == HIGH && fromMaster.available()) {
    String line = fromMaster.readStringUntil('\n');
    line.trim();

    SlaveCommand cmd;
    if (parsePacket(line, cmd)) {

      // เช็คว่า packet นี้ของเราไหม
      if (cmd.wheel == MY_WHEEL) {
        Serial.printf("[W%d] timer:%d kp:%.1f ki:%.1f kd:%.1f rpm:%d\n",
                      cmd.wheel, cmd.timer,
                      cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);

        // ใส่ logic ควบคุม motor ที่นี่
      }
    }
  }
}