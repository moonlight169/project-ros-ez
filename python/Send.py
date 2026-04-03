import socket

class ESPSender:
    def __init__(self, ip="192.168.1.177", port=8888):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # ตั้งค่าคงที่ PID และ Resolution พื้นฐาน (ปรับแก้ได้ที่นี่)
        self.p_val = 1.0
        self.i_val = 1.0
        self.d_val = 1.0
        self.r_val = 200

    def send_rpm(self, rpm_fl, rpm_fr, rpm_rl, rpm_rr):
        """
        รับค่า RPM ทั้ง 4 ล้อ จัด Format แล้วส่งผ่าน UDP
        """
        # เพิ่มตัวแปร timer ที่คุณใช้ใน ESP32 (เช่น 160)
        self.timer_val = 160 
        
        # จัดรูปแบบใหม่ให้ตรงกับ C++ -> [wheel, timer, p, i, d, target_rpm]
        # สังเกตว่าเราใช้ int() ครอบ rpm เพื่อตัดทศนิยมทิ้งไปเลย ข้อมูลจะได้สั้นๆ
        data_packet = (
            f"[[1,{self.timer_val},{self.p_val},{self.i_val},{self.d_val},{int(rpm_fl)}], "
            f"[2,{self.timer_val},{self.p_val},{self.i_val},{self.d_val},{int(rpm_fr)}], "
            f"[3,{self.timer_val},{self.p_val},{self.i_val},{self.d_val},{int(rpm_rl)}], "
            f"[4,{self.timer_val},{self.p_val},{self.i_val},{self.d_val},{int(rpm_rr)}]]"
        )
        
        try:
            self.sock.sendto(data_packet.encode('utf-8'), (self.ip, self.port))
            return data_packet
        except Exception as e:
            print(f"Error sending UDP: {e}")
            return None

    def close(self):
        """ปิดการเชื่อมต่อ Socket"""
        self.sock.close()

# --- ทดสอบการทำงานของไฟล์นี้แบบเดี่ยวๆ ---
if __name__ == "__main__":
    test_sender = ESPSender(ip="192.168.1.177", port=8888)
    print("Testing UDP Sender...")
    packet_sent = test_sender.send_rpm(100.5, 100.5, -100.5, -100.5)
    print(f"Sent: {packet_sent}")
    test_sender.close()
    print("Socket closed.")