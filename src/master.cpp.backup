#include <Arduino.h>
#include <HardwareSerial.h>

// === PIN CONFIG ===
const int PIN_ALL = 4;                  // ขา Enable (ส่งสัญญาณบอก Slave ทุกตัว)
const int TX_PINS[4] = {13, 27, 26, 25}; // ขาส่งแยกไป Slave 1, 2, 3, 4

HardwareSerial SlaveSerial(1); // ใช้ Hardware UART ชุดที่ 1

struct SlaveCommand {
  int   wheel;
  int   timer;
  float kp, ki, kd;
  int   rpm_in;
};

// ฟังก์ชันส่งข้อมูลโดยการสลับขา TX ตามดัชนี (idx 0-3)
void sendToSlave(int idx, SlaveCommand cmd) {
  SlaveSerial.end(); 
  SlaveSerial.begin(9600, SERIAL_8N1, -1, TX_PINS[idx]);

  char buf[64];
  // รูปแบบ: [wheel,timer,kp,ki,kd,rpm]
  snprintf(buf, sizeof(buf), "[%d,%d,%.1f,%.1f,%.1f,%d]\n",
           cmd.wheel, cmd.timer,
           cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);

  digitalWrite(PIN_ALL, HIGH); // ดึงขา 4 เป็น HIGH เพื่อสะกิด Slave
  SlaveSerial.print(buf);      // ส่งข้อมูลออกไป
  SlaveSerial.flush();         // รอจนข้อมูลออกจาก Buffer หมด
  digitalWrite(PIN_ALL, LOW);  // ดึงขา 4 กลับเป็น LOW

  Serial.printf("[TX→S%d] %s", idx + 1, buf);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ALL, OUTPUT);
  digitalWrite(PIN_ALL, LOW);
  
  Serial.println("Master Command Center - Start");
}

void loop() {
  // วนส่งให้ Slave 1 ถึง 4
  for (int i = 0; i < 4; i++) {
    SlaveCommand cmd;
    cmd.wheel  = i + 1; // 1, 2, 3, 4
    cmd.timer  = 160;   // ค่าคงที่
    cmd.kp     = 1.0;   // ค่าคงที่ (ปรับแก้ได้ที่นี่)
    cmd.ki     = 1.0;
    cmd.kd     = 1.0;
    cmd.rpm_in = 250;   // ค่า RPM คงที่ (หรือเปลี่ยนเป็นตัวแปรอื่นตามต้องการ)

    sendToSlave(i, cmd);
    delay(50); // หน่วงเวลาสั้นๆ ระหว่างการสลับตัวส่ง
  }

  delay(1000); // ส่งชุดคำสั่งซ้ำทุก 1 วินาที
}