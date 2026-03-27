#include <Arduino.h>
#include <HardwareSerial.h>

const int PIN_ALL = 4;
const int TX_PINS[4] = {13, 27, 26, 25};

HardwareSerial SlaveSerial(1);

struct SlaveCommand {
  int   wheel, timer;
  float kp, ki, kd;
  int   rpm_in;
};

struct SlaveFeedback {
  int wheel, timer, rpm_out;
  bool valid;
};

// ส่งคำสั่ง แล้วสลับ RX รอรับ feedback ทันที
SlaveFeedback sendAndReceive(int idx, SlaveCommand cmd) {
  SlaveFeedback fb = {0, 0, 0, false};

  // --- ขาส่ง ---
  SlaveSerial.end();
  SlaveSerial.begin(9600, SERIAL_8N1, -1, TX_PINS[idx]); // TX only

  char buf[64];
  snprintf(buf, sizeof(buf), "[%d,%d,%.1f,%.1f,%.1f,%d]\n",
           cmd.wheel, cmd.timer, cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);

  digitalWrite(PIN_ALL, HIGH);
  SlaveSerial.print(buf);
  SlaveSerial.flush();
  digitalWrite(PIN_ALL, LOW);

  // --- สลับเป็นขารับ (สายเดิม กลับทิศ) ---
  SlaveSerial.end();
  SlaveSerial.begin(9600, SERIAL_8N1, TX_PINS[idx], -1); // RX only

  delay(50); // รอ Slave ประมวลผล + สลับ TX

  // อ่าน feedback พร้อม timeout
  unsigned long t0 = millis();
  String line = "";
  while (millis() - t0 < 50) {
    if (SlaveSerial.available()) {
      line = SlaveSerial.readStringUntil('\n');
      line.trim();
      if (line.length() > 0) break;
    }
  }

  // parse [wheel,timer,rpm_out]
  if (line.startsWith("[") && line.endsWith("]")) {
    line.replace("[", ""); line.replace("]", "");
    String tok[3]; int ti = 0;
    for (char c : line) {
      if (c == ',') { ti++; if (ti >= 3) goto done; }
      else tok[ti] += c;
    }
    if (ti == 2) {
      fb.wheel   = tok[0].toInt();
      fb.timer   = tok[1].toInt();
      fb.rpm_out = tok[2].toInt();
      fb.valid   = true;
    }
  }
  done:
  Serial.printf("[S%d] TX→[%s] | FB←[w:%d t:%d rpm:%d] %s\n",
    idx+1, buf[0] == '[' ? buf+1 : buf,
    fb.wheel, fb.timer, fb.rpm_out,
    fb.valid ? "OK" : "TIMEOUT");
  return fb;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ALL, OUTPUT);
  digitalWrite(PIN_ALL, LOW);
}

void loop() {
  Serial.printf("=== Sending commands to Slaves ===\n");
  for (int i = 0; i < 4; i++) {
   
    SlaveCommand cmd = {i+1, 160+i, 1.0, 1.0, 1.0, 250};
    SlaveFeedback fb = sendAndReceive(i, cmd);

    // ใช้ fb.rpm_out ทำ PID หรือ logic อื่นที่นี่

    delay(50);
  }
  delay(3000);
}