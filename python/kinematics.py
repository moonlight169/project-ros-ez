class MecanumKinematics:
    def __init__(self, wheel_radius=1.0, lx=1.0, ly=1.0):
        # คุณสามารถใส่ค่าระยะห่างของล้อถึงจุดศูนย์กลาง (Lx, Ly) และรัศมีล้อได้
        # เพื่อให้สมการออกมาเป็นความเร็วมอเตอร์ที่แม่นยำ (RPM หรือ Rad/s)
        # แต่ถ้าตั้งเป็น 1.0 จะเป็นการคำนวณสัดส่วนความเร็วแบบดิบๆ (Raw PWM ratio)
        self.wheel_radius = wheel_radius
        self.lx = lx
        self.ly = ly

    def calculate(self, linear_x, linear_y, angular_z):
        """
        แปลงค่า cmd_vel เป็นความเร็วล้อทั้ง 4
        """
        # ตัวคูณระยะห่างจากจุดศูนย์กลาง
        z_factor = angular_z * (self.lx + self.ly)

        # คำนวณความเร็วแต่ละล้อตามสมการ Mecanum
        # หมายเหตุ: เครื่องหมาย +/- อาจต้องสลับตามการวางขั้วมอเตอร์และทิศของลูกกลิ้งบนล้อ
        v_fl = linear_x - linear_y - z_factor
        v_fr = linear_x + linear_y + z_factor
        v_rl = linear_x + linear_y - z_factor
        v_rr = linear_x - linear_y + z_factor

        return {
            "FL": v_fl,  # Front Left
            "FR": v_fr,  # Front Right
            "RL": v_rl,  # Rear Left
            "RR": v_rr   # Rear Right
        }

if __name__ == "__main__":
    kinematics = MecanumKinematics()
    
    # ลองจำลองว่าสั่งให้รถสไลด์ไปทางซ้าย (Y เป็นบวก)
    test_cmd = kinematics.calculate(linear_x=0.0, linear_y=1.0, angular_z=0.0)
    
    print("Test Strafing Left:")
    print(f"Front-Left  (FL) : {test_cmd['FL']:>5.1f}")
    print(f"Front-Right (FR) : {test_cmd['FR']:>5.1f}")
    print(f"Rear-Left   (RL) : {test_cmd['RL']:>5.1f}")
    print(f"Rear-Right  (RR) : {test_cmd['RR']:>5.1f}")