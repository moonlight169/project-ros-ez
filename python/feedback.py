import socket
import time
import os

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# ตัวแปรสำหรับคำนวณ Hz
prev_time = time.time()
counter = 0
hz = 0
last_feedback = ""

# ถ้าคุณต้องการโชว์สิ่งที่ส่งไปล่าสุดในไฟล์นี้ด้วย 
# ปกติถ้าส่งจากอีกไฟล์ (Input_KB) ไฟล์นี้จะไม่รู้ 
# ยกเว้นเราจะพิมพ์ทิ้งไว้หรือใช้ระบบแชร์ข้อมูล 
last_sent = "Waiting..." 

print("--- System Monitoring Started ---")

try:
    while True:
        # 1. รับข้อมูล Feedback จาก ESP32
        data, addr = sock.recvfrom(1024)
        last_feedback = data.decode('utf-8')
        
        # 2. คำนวณ Hz
        counter += 1
        current_time = time.time()
        elapsed = current_time - prev_time
        
        if elapsed >= 1.0:
            hz = counter / elapsed
            counter = 0
            prev_time = current_time

        # 3. แสดงผล Output แบบบรรทัดเดียว (ใช้ \r เพื่อให้มันทับที่เดิม)
        # Format: Hz: 82.5 | sent [x,x,x,x,x,x] | feedback [x,x,x]|[x,x,x]...
        output = f"\rHz: {hz:6.2f} | feedback {last_feedback}"
        
        # พิมพ์ออกแบบไม่ขึ้นบรรทัดใหม่
        print(output)

except KeyboardInterrupt:
    print("\n--- Stopped ---")
finally:
    sock.close()