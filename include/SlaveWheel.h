#ifndef SLAVE_WHEEL_H  // ป้องกันการดึงไฟล์ซ้ำ
#define SLAVE_WHEEL_H

#include <Arduino.h>

struct SlaveCommand {
    int wheel, timer;
    float kp, ki, kd;
    int rpm_in;
};

struct SlaveFeedback {
    int wheel = 0;
    int timer = 0;
    int rpm_out = 0;
    bool valid = false;
    char raw[32] = ""; 
};

class SlaveWheel {
private:
    int _idx;
    int _txPin;
    SlaveFeedback _lastFb;

public:
    SlaveWheel(int index, int txPin) : _idx(index), _txPin(txPin) {}

    // ฟังก์ชันอัปเดตข้อมูลมอเตอร์
    void update(SlaveCommand cmd, HardwareSerial &serial, int pinAll) {
        _lastFb.valid = false;
        char txBuf[64];
        snprintf(txBuf, sizeof(txBuf), "[%d,%d,%.1f,%.1f,%.1f,%d]", 
                 cmd.wheel, cmd.timer, cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);

        serial.end();
        serial.begin(2000000, SERIAL_8N1, -1, _txPin);
        
        digitalWrite(pinAll, HIGH);
        serial.println(txBuf);
        serial.flush();
        digitalWrite(pinAll, LOW);

        serial.end();
        serial.begin(2000000, SERIAL_8N1, _txPin, -1);

        unsigned long t0 = millis();
        int pos = 0;
        while (millis() - t0 < 5) {
            while (serial.available()) {
                char c = serial.read();
                if (c == '\n') {
                    _lastFb.raw[pos] = '\0';
                    if (sscanf(_lastFb.raw, "[%d,%d,%d]", &_lastFb.wheel, &_lastFb.timer, &_lastFb.rpm_out) == 3) {
                        _lastFb.valid = true;
                    }
                    return;
                }
                if (pos < 31) _lastFb.raw[pos++] = c;
            }
        }
    }

    SlaveFeedback getFeedback() const { return _lastFb; }
};

#endif