#include <Arduino.h>
#include <HardwareSerial.h>
#include "SlaveWheel.h"
#include "NetworkConfig.h"

const int PIN_ALL = 4;
HardwareSerial SlaveSerial(1);

SlaveWheel wheels[4] = {
    SlaveWheel(1, 13), 
    SlaveWheel(2, 27), 
    SlaveWheel(3, 26), 
    SlaveWheel(4, 25)
};

// จอง Memory ไว้ล่วงหน้าเพื่อลดภาระ CPU ใน loop
char globalBuffer[512]; 

void setup() {
    // Serial สำหรับ Debug ยังเปิดไว้ได้ แต่ใน loop จะไม่สั่ง print
    Serial.begin(115200);
    pinMode(PIN_ALL, OUTPUT);
    setupNetwork();
    
    // เคลียร์ buffer เริ่มต้น
    memset(globalBuffer, 0, sizeof(globalBuffer));
}

void loop() {
    int offset = 0;

    for (int i = 0; i < 4; i++) {
        SlaveCommand cmd = {i + 1, 160, 1.0f, 1.0f, 1.0f, 250};
        wheels[i].update(cmd, SlaveSerial, PIN_ALL);
        
        SlaveFeedback fb = wheels[i].getFeedback();
        
        // ใช้ snprintf เขียนลง globalBuffer โดยตรง (เร็วกว่า String +=)
        int written = 0;
        if (fb.valid) {
            written = snprintf(globalBuffer + offset, sizeof(globalBuffer) - offset, 
                               "[%d,%d,%.1f,%.1f,%.1f,%d,%d]", 
                               cmd.wheel, cmd.timer, cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in, fb.rpm_out);
        } else {
            written = snprintf(globalBuffer + offset, sizeof(globalBuffer) - offset, 
                               "[%d,%d,%.1f,%.1f,%.1f,%d,?]", 
                               cmd.wheel, cmd.timer, cmd.kp, cmd.ki, cmd.kd, cmd.rpm_in);
        }
        
        offset += written;
        if (i < 3 && offset < (int)sizeof(globalBuffer) - 1) {
            globalBuffer[offset++] = '|';
        }
    }

    // ส่ง Packet ทันที
    if (offset > 0) {
        globalBuffer[offset] = '\0'; // ปิดท้าย string
        sendPacket(globalBuffer); 
    }

    // ไม่ต้องมี delay, ไม่ต้องมี Serial.print
    // loop นี้จะวิ่งซ้ำทันทีที่ส่ง Packet เสร็จ
}