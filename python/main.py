import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("--- Data Monitoring Started ---")

while True:
    data, addr = sock.recvfrom(1024)
    raw_msg = data.decode('utf-8')
    
    # แยกข้อมูลแต่ละล้อด้วย |
    wheels_data = raw_msg.split('|')
    
    print("-" * 50)
    for wheel_msg in wheels_data:
        # wheel_msg จะมีหน้าตาแบบ [1,160,1.0,1.0,1.0,250,248]
        # เอา [ ] ออกแล้วแยกด้วย ,
        clean_msg = wheel_msg.replace('[', '').replace(']', '')
        parts = clean_msg.split(',')
        
        if len(parts) == 7:
            w_id, timer, kp, ki, kd, target, actual = parts
            print(f"Wheel {w_id} | Target: {target} | Actual: {actual} | PID: {kp},{ki},{kd}")