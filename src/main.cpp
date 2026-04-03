#include <Arduino.h>
#include <HardwareSerial.h>
#include "SlaveWheel.h"
#include "NetworkConfig.h"

// --- Configuration ---
const int PIN_ALL = 4;
HardwareSerial SlaveSerial(1);

// โครงสร้างเก็บสถานะปัจจุบันของแต่ละล้อ
struct DataLoop {
    int timer = 160;
    float kp = 1.0f, ki = 1.0f, kd = 1.0f;
    int rpm_in = 0;
} wheelParams[4];

// สร้าง Object ควบคุมล้อ
SlaveWheel wheels[4] = {
    SlaveWheel(1, 13), SlaveWheel(2, 27), SlaveWheel(3, 26), SlaveWheel(4, 25)
};

// Buffer สำหรับรวมข้อมูลส่งกลับ
char allWheelsStatus[512]; 

void setup() {
    // Serial.begin(115200);
    pinMode(PIN_ALL, OUTPUT);
    
    // ตั้งค่า W5500 (NetworkConfig.h)
    setupNetwork();
    
    Serial.println(">>> ESP32 Multi-Wheel System Ready <<<");
}

void loop() {
    // --- 1. รับคำสั่งจาก Windows (แบบ Multi-Array [[...],[...]]) ---
    int len = Udp.parsePacket(); // แก้รับค่าจาก Udp.parsePacket() ให้ตรงกับขนาดข้อมูล
    if (len > 0) {
        char rawCommand[256]; 
        int bytesRead = Udp.read(rawCommand, 255);
        if (bytesRead > 0) {
            rawCommand[bytesRead] = '\0';

            char* ptr = rawCommand;
            while ((ptr = strchr(ptr, '[')) != NULL) {
                ptr++; 
                if (*ptr == '[') continue; 

                int w_idx, t_timer;
                float t_kp, t_ki, t_kd, t_rpm; // เปลี่ยน t_rpm ให้เป็น float ก่อน

                // คัดแยกข้อมูล: [wheel, timer, kp, ki, kd, rpm]
                // ใช้ %f กับ t_rpm เพื่อรองรับเลขทศนิยมจาก Python
                if (sscanf(ptr, "%d,%d,%f,%f,%f,%f", 
                           &w_idx, &t_timer, &t_kp, &t_ki, &t_kd, &t_rpm) == 6) {
                    
                    if (w_idx >= 1 && w_idx <= 4) {
                        int i = w_idx - 1;
                        wheelParams[i].timer = t_timer;
                        wheelParams[i].kp = t_kp;
                        wheelParams[i].ki = t_ki;
                        wheelParams[i].kd = t_kd;
                        
                        // แปลง float ทศนิยมให้เป็น int ให้มอเตอร์นำไปใช้
                        wheelParams[i].rpm_in = (int)t_rpm; 
                    }
                }
                
                ptr = strchr(ptr, ']');
                if (ptr == NULL) break;
            }
        }
    }
    // --- 2. อัปเดตล้อทุกล้อ & เตรียม Feedback ---
    int writePos = 0;
    // เคลียร์ buffer ก่อนเขียนใหม่
    allWheelsStatus[0] = '\0';

    for (int i = 0; i < 4; i++) {
        // ใช้ค่าล่าสุดที่อยู่ใน wheelParams สั่งงาน
        SlaveCommand cmd = {
            i + 1, 
            wheelParams[i].timer, 
            wheelParams[i].kp, 
            wheelParams[i].ki, 
            wheelParams[i].kd, 
            wheelParams[i].rpm_in
        };
        
        // คุยกับ Slave (Serial)
        wheels[i].update(cmd, SlaveSerial, PIN_ALL);
        
        // รับค่าตอบกลับ
        SlaveFeedback fb = wheels[i].getFeedback();
        
        // รวมร่าง Feedback: [wheel, time, rpm_out]
        // เปลี่ยน Format การโชว์ ให้เห็นทั้ง in และ out
        int written = snprintf(allWheelsStatus + writePos, sizeof(allWheelsStatus) - writePos, 
                       "[%d,%d,In:%d,Out:%d]%s", 
                       i + 1, 
                       wheelParams[i].timer, 
                       wheelParams[i].rpm_in,      // โชว์ค่าที่รับมาจาก Python
                       fb.valid ? fb.rpm_out : -1, // โชว์ค่าจริงที่ล้อหมุนอยู่
                       (i < 3) ? "|" : "");
        writePos += written;
    }

    // --- 3. ส่งกลับ Windows (UDP) ---
    if (writePos > 0) {
        sendPacket(allWheelsStatus); 
    }

}