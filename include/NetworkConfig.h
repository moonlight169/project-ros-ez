#ifndef NETWORK_CONFIG_H
#define NETWORK_CONFIG_H

#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

// IP ของ ESP32 (ต้องเป็นวง 192.168.1.x เหมือนคอม)
inline byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
inline IPAddress ip(192, 168, 1, 177); 
inline IPAddress destIP(192, 168, 1, 10); // IP เครื่อง Windows ของคุณ
inline unsigned int destPort = 5005;

inline EthernetUDP Udp;

inline void setupNetwork() {
    // สำหรับ ESP32 + W5500 ปกติใช้ CS Pin 5
    Ethernet.init(5); 
    Ethernet.begin(mac, ip);
    Udp.begin(8888);
}

inline void sendPacket(String msg) {
    Udp.beginPacket(destIP, destPort);
    Udp.print(msg);
    Udp.endPacket();
}

#endif