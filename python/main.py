# นำเข้าโค้ดจากไฟล์คีย์บอร์ดของคุณ
import Input_kb_mac 
from kinematics import MecanumKinematics
from speed_to_rpm import SpeedToRPM
import python.Send as Send

kinematics = MecanumKinematics()
converter = SpeedToRPM(wheel_radius=0.1016)
esp_sender = Send.ESPSender(ip="192.168.1.177", port=8888)

def on_receive_cmd_vel():
    """ฟังก์ชันนี้จะดึงค่าจากไฟล์คีย์บอร์ดมาคำนวณและส่งข้อมูล"""
    current_vel = Input_kb_mac.cmd_vel
    
    # 1. ส่งเข้าสมการ Kinematics (ได้ผลลัพธ์เป็น m/s)
    wheel_speeds = kinematics.calculate(
        linear_x=current_vel["linear_x"],
        linear_y=current_vel["linear_y"],
        angular_z=current_vel["angular_z"]
    )
    
    # 2. แปลงความเร็ว m/s เป็น RPM
    rpm_fl = converter.convert(wheel_speeds['FL'])
    rpm_fr = converter.convert(wheel_speeds['FR'])
    rpm_rl = converter.convert(wheel_speeds['RL'])
    rpm_rr = converter.convert(wheel_speeds['RR'])
    
    # 3. ส่งข้อมูลผ่าน UDP ไปยัง ESP32 และรับข้อความที่แพ็กแล้วกลับมาโชว์
    data_packet = esp_sender.send_rpm(rpm_fl, rpm_fr, rpm_rl, rpm_rr)
    
    # 4. พิมพ์ผลลัพธ์บนจอคอม (เปลี่ยนมาโชว์ค่า RPM ให้ถูกต้อง)
    print(f"\n--- Motor Speeds (RPM) ---")
    print(f" FL: {wheel_speeds['FL']:>6.2f} | FR: {wheel_speeds['FR']:>6.2f}")
    print(f" RL: {wheel_speeds['RL']:>6.2f} | RR: {wheel_speeds['RR']:>6.2f}")
    print(f" [Sent Packet] -> {data_packet}")
    print(f"--------------------------")

if __name__ == "__main__":
    if hasattr(Input_kb_mac, 'starts_ui'):
        Input_kb_mac.starts_ui() 
        
    Input_kb_mac.print_status = on_receive_cmd_vel
    
    print(f"--- Robot Controller Ready ---")
    print(f"Target ESP32 -> {esp_sender.ip}:{esp_sender.port}")
    print("------------------------------")
    
    try:
        # เริ่มรันคีย์บอร์ด (Block การทำงาน)
        Input_kb_mac.main()
    except KeyboardInterrupt:
        pass
    finally:
        # เมื่อกด Ctrl+C เพื่อออกโปรแกรม ค่อยสั่งปิด Socket ตรงนี้ครับ
        esp_sender.close()
        print("\nSocket Closed. Goodbye!")