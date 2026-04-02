import socket

ESP_IP = "192.168.1.177"
ESP_PORT = 8888 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("--- Sender [wheel, time, kp, ki, kd, rpm_in] ---")
print("Example: 1,160,1.0,1.0,1.0,250")

try:
    while True:
        val = input("\nEnter Data: ") # พิมพ์เลข 6 ตัวคั่นด้วยคอมม่า
        if val.lower() == 'q': break
        
        # จัด Format ให้เป็น [1,160,1.0,1.0,1.0,250]
        cmd = f"[{val}]"
        sock.sendto(cmd.encode(), (ESP_IP, ESP_PORT))
        print(f"Sent to ESP32 >> {cmd}")
except KeyboardInterrupt:
    pass
finally:
    sock.close()