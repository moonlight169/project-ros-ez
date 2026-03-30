#include <Arduino.h>
#include <HardwareSerial.h>

const int  PIN_ALL     = 4;
const int  TX_PINS[4]  = {13, 27, 26, 25};
const long BAUD        = 115200;
const int  RX_TIMEOUT  = 12;

HardwareSerial SlaveSerial(1);

struct SlaveCommand {
  int   wheel, timer;
  float kp, ki, kd;
  int   rpm_in;
};

struct SlaveFeedback {
  int  wheel, timer, rpm_out;
  bool valid;
};

// ── Hz tracking ───────────────────────────────────────
unsigned long loopCount   = 0;
unsigned long lastHzPrint = 0;
unsigned long lastLoopUs  = 0;
// ──────────────────────────────────────────────────────

SlaveFeedback sendAndReceive(int idx, SlaveCommand cmd) {
  SlaveFeedback fb = {0, 0, 0, false};

  // ── TX phase ──────────────────────────────────────────
  SlaveSerial.end();
  SlaveSerial.begin(BAUD, SERIAL_8N1, -1, TX_PINS[idx]);

  char buf[48];
  int len = snprintf(buf, sizeof(buf),
    "[%d,%d,%.2f,%.2f,%.2f,%d]\n",
    cmd.wheel, cmd.timer,
    cmd.kp, cmd.ki, cmd.kd,
    cmd.rpm_in);

  digitalWrite(PIN_ALL, HIGH);
  SlaveSerial.write((uint8_t*)buf, len);
  SlaveSerial.flush();
  digitalWrite(PIN_ALL, LOW);

  // ── RX phase ──────────────────────────────────────────
  SlaveSerial.end();
  SlaveSerial.begin(BAUD, SERIAL_8N1, TX_PINS[idx], -1);

  char line[32];
  int  pos = 0;
  unsigned long t0 = millis();

  while (millis() - t0 < RX_TIMEOUT) {
    while (SlaveSerial.available()) {
      char c = SlaveSerial.read();
      if (c == '\n') { line[pos] = '\0'; goto parse; }
      if (pos < 31) line[pos++] = c;
    }
  }
  goto done;

parse:
  if (sscanf(line, "[%d,%d,%d]",
      &fb.wheel, &fb.timer, &fb.rpm_out) == 3) {
    fb.valid = true;
  }

done:
  return fb;  // ไม่มี Serial.printf ที่นี่ → ไม่เสียเวลา
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ALL, OUTPUT);
  digitalWrite(PIN_ALL, LOW);
  delay(500);
  Serial.println("Master ready");
  lastHzPrint = millis();
}

void loop() {
  unsigned long loopBegin = micros();

  SlaveFeedback results[4];
  for (int i = 0; i < 4; i++) {
    SlaveCommand cmd = {i + 1, 160, 1.0f, 1.0f, 1.0f, 250};
    results[i] = sendAndReceive(i, cmd);

    // ── ใส่ PID logic ที่นี่ ──
    // if (results[i].valid) { ... }
  }

  lastLoopUs = micros() - loopBegin;
  loopCount++;

  // ── พิมพ์ Hz + feedback ทุก 1 วินาที ──────────────────
  unsigned long now = millis();
  if (now - lastHzPrint >= 1000) {
    float elapsed = (now - lastHzPrint) / 1000.0f;
    float hz      = loopCount / elapsed;

    Serial.println("==============================");
    Serial.printf("Hz      : %.1f\n", hz);
    Serial.printf("loop    : %lu us (%.2f ms)\n",
                  lastLoopUs, lastLoopUs / 1000.0f);
    Serial.println("------------------------------");
    for (int i = 0; i < 4; i++) {
      Serial.printf("S%d: rpm=%d timer=%d %s\n",
        i + 1,
        results[i].rpm_out,
        results[i].timer,
        results[i].valid ? "OK" : "TIMEOUT");
    }
    Serial.println("==============================");

    loopCount   = 0;
    lastHzPrint = now;
  }
}