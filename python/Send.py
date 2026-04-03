import socket

ESP_IP = "192.168.1.177"
ESP_PORT = 8888 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("--- Multi-Wheel Sender ---")
print("Format: [[w,t,p,i,d,r], [w,t,p,i,d,r]]")

try:
    while True:
        # พิมพ์: [[1,160,1,1,1,200], [3,200,1,1,1,150]]
        val = input("\n>> Send Multi-Array: ") 
        if val.lower() == 'q': break
        
        sock.sendto(val.encode(), (ESP_IP, ESP_PORT))
        print(f"Sent: {val}")
except:
    pass
finally:
    sock.close()