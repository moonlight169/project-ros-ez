# นำเข้าโค้ดจากไฟล์คีย์บอร์ดของคุณ (สมมติว่าไฟล์ชื่อ Input_kb_mac.py)
import Input_kb_mac 
from kinematics import MecanumKinematics

# สร้างตัวคำนวณ
kinematics = MecanumKinematics()

def on_receive_cmd_vel():
    """ฟังก์ชันนี้จะดึงค่าจากไฟล์คีย์บอร์ดมาคำนวณ"""
    # ดึงค่าปัจจุบันออกมาจาก Input_kb_mac
    current_vel = Input_kb_mac.cmd_vel
    
    # ส่งเข้าสมการ Kinematics
    wheel_speeds = kinematics.calculate(
        linear_x=current_vel["linear_x"],
        linear_y=current_vel["linear_y"],
        angular_z=current_vel["angular_z"]
    )
    
    # พิมพ์ผลลัพธ์ความเร็วของมอเตอร์ทั้ง 4 ล้อ
    print(f"\n--- Motor Speeds ---")
    print(f" FL: {wheel_speeds['FL']:>5.1f} | FR: {wheel_speeds['FR']:>5.1f}")
    print(f" RL: {wheel_speeds['RL']:>5.1f} | RR: {wheel_speeds['RR']:>5.1f}")
    print(f"--------------------")
    
    # TODO: นำค่า wheel_speeds ที่ได้ไปสั่งงานมอเตอร์ (PWM) หรือส่งผ่าน Serial ต่อไป


if __name__ == "__main__":
    Input_kb_mac.starts_ui() 
    Input_kb_mac.print_status = on_receive_cmd_vel
    
    # เริ่มรันคีย์บอร์ด
    Input_kb_mac.main()