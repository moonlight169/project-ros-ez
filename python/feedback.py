import socket
import time
import re

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# ตัวแปรสำหรับคำนวณ Hz
prev_time = time.time()
counter = 0
hz = 0

print("--- System Monitoring Started ---")
print("Format: Hz | [[wheel, timer, rpm_out], ...]")
print("-" * 80)

try:
    while True:
        # 1. รับข้อมูล Feedback จาก ESP32
        # Expected format: [wheel,timer,rpm_out]|[wheel,timer,rpm_out]|...
        data, addr = sock.recvfrom(1024)
        feedback_str = data.decode('utf-8').strip()
        
        # 2. คำนวณ Hz
        counter += 1
        current_time = time.time()
        elapsed = current_time - prev_time
        
        if elapsed >= 1.0:
            hz = counter / elapsed
            counter = 0
            prev_time = current_time
        
        # 3. Parse feedback และคำนวณ round-trip time
        # Regex pattern: [wheel, timer, rpm_out]
        pattern = r'\[(\d+),(\d+),(-?\d+)\]'
        matches = re.findall(pattern, feedback_str)
        
        if matches:
            # ส่วนแสดงผล
            output_array = []
            
            for wheel, sent_timer_str, rpm_out in matches:
                sent_timer = int(sent_timer_str)
                output_array.append([int(wheel), sent_timer, int(rpm_out)])
            
            # 4. แสดงผล Output แบบใหม่
            output = f"{hz:6.2f} | {output_array}"
            print(output)
        else:
            print(f"\rNo valid feedback: {feedback_str}")

except KeyboardInterrupt:
    print("\n--- Stopped ---")
finally:
    sock.close()