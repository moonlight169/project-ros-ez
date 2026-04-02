#include <Arduino.h>
#include <HardwareSerial.h>
#include "SlaveWheel.h"
#include "NetworkConfig.h"

const int PIN_ALL = 4;
HardwareSerial SlaveSerial(1);

// ตัวแปรส่วนกลางสำหรับล้อทั้ง 4
struct ControlParam {
    int timer = 160;
    float kp = 1.0, ki = 1.0, kd = 1.0;
    int rpm_in = 0;
} wheelParams[4];

SlaveWheel wheels[4] = {
    SlaveWheel(1, 13), SlaveWheel(2, 27), SlaveWheel(3, 26), SlaveWheel(4, 25)
};

char globalBuffer[512]; 

void setup() {
    Serial.begin(115200);
    pinMode(PIN_ALL, OUTPUT);
    setupNetwork();
    Serial.println("ESP32 Wheel System Ready...");
}

void loop() {
    int packetSize = Udp.parsePacket();
    if (packetSize) {
        char rxBuf[128];
        int len = Udp.read(rxBuf, 127);
        if (len > 0) {
            rxBuf[len] = 0;
            int w_idx, t_timer, t_rpm;
            float t_kp, t_ki, t_kd;
            
            if (sscanf(rxBuf, "[%d,%d,%f,%f,%f,%d]", &w_idx, &t_timer, &t_kp, &t_ki, &t_kd, &t_rpm) == 6) {
                if (w_idx >= 1 && w_idx <= 4) {
                    // แก้ไขจุดที่พังตรงนี้ครับ
                    int i = w_idx - 1;
                    wheelParams[i].timer = t_timer;
                    wheelParams[i].kp = t_kp;
                    wheelParams[i].ki = t_ki;
                    wheelParams[i].kd = t_kd;
                    wheelParams[i].rpm_in = t_rpm;
                }
            }
        }
    }

    // --- 2. อัปเดตล้อ & เตรียม Feedback [wheel, time, rpm_out] ---
    int offset = 0;
    for (int i = 0; i < 4; i++) {
        SlaveCommand cmd = {i + 1, wheelParams[i].timer, wheelParams[i].kp, wheelParams[i].ki, wheelParams[i].kd, wheelParams[i].rpm_in};
        wheels[i].update(cmd, SlaveSerial, PIN_ALL);
        
        SlaveFeedback fb = wheels[i].getFeedback();
        
        // ส่งกลับเฉพาะ [wheel, time, rpm_out]
        offset += snprintf(globalBuffer + offset, sizeof(globalBuffer) - offset, 
                           "[%d,%d,%d]%s", 
                           i + 1, wheelParams[i].timer, fb.valid ? fb.rpm_out : -1,
                           (i < 3) ? "|" : "");
    }

    // --- 3. ส่งกลับ Windows ---
    sendPacket(globalBuffer); 
}