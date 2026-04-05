class MecanumKinematics:
    def __init__(self, wheel_radius=0.0508, lx=0.15, ly=0.15):
        """
        Mecanum Wheel Kinematics
        
        Args:
            wheel_radius: รัศมีล้อ (ม) - ค่าเริ่มต้น 0.0508 ม (4 นิ้ว)
            lx: ระยะห่างล้อถึงจุดศูนย์กลาง (แกน X) (ม)
            ly: ระยะห่างล้อถึงจุดศูนย์กลาง (แกน Y) (ม)
        """
        self.wheel_radius = wheel_radius
        self.lx = lx
        self.ly = ly

    def calculate(self, linear_x, linear_y, angular_z, normalize=False):
        """
        แปลงค่า cmd_vel เป็นความเร็วล้อทั้ง 4
        
        Args:
            linear_x: ความเร็วเชิงเส้น X (ไปข้างหน้า-หลัง)
            linear_y: ความเร็วเชิงเส้น Y (สไลด์ซ้าย-ขวา)
            angular_z: ความเร็วเชิงมุม (หันตัวหนึ่ง)
            normalize: normalize ความเร็วสูงสุดให้ = 1.0 (สำหรับ PWM 0-255)
        """
        # ตัวคูณระยะห่างจากจุดศูนย์กลาง
        z_factor = angular_z * (self.lx + self.ly)

        # คำนวณความเร็วแต่ละล้อตามสมการ Mecanum
        v_fl = linear_x - linear_y - z_factor
        v_fr = linear_x + linear_y + z_factor
        v_rl = linear_x + linear_y - z_factor
        v_rr = linear_x - linear_y + z_factor

        wheels = {
            "FL": v_fl,  # Front Left
            "FR": v_fr,  # Front Right
            "RL": v_rl,  # Rear Left
            "RR": v_rr   # Rear Right
        }
        
        # Normalize ถ้าจำเป็น (เพื่อให้ความเร็วสูงสุด = 1.0)
        if normalize:
            max_speed = max(abs(v) for v in wheels.values())
            if max_speed > 0:
                wheels = {k: v / max_speed for k, v in wheels.items()}
        
        return wheels

if __name__ == "__main__":
    # ล้อผ่านศูนย์กลาง 4 นิ้ว (0.0508 ม), ระยะ Lx=Ly=0.15 ม
    kinematics = MecanumKinematics(wheel_radius=0.0508, lx=0.15, ly=0.15)
    
    print("=" * 50)
    print("Mecanum Kinematics Test")
    print("=" * 50)
    print(f"Wheel Radius: {kinematics.wheel_radius*1000:.1f} mm")
    print(f"Distance lx, ly: {kinematics.lx:.3f}m\n")
    
    # Test 1: สไลด์ไปทางซ้าย (Y เป็นบวก)
    result = kinematics.calculate(linear_x=0.0, linear_y=1.0, angular_z=0.0)
    print("Test 1: Strafing Left (vx=0, vy=1.0, wz=0)")
    print(f"  FL: {result['FL']:>6.2f}  FR: {result['FR']:>6.2f}")
    print(f"  RL: {result['RL']:>6.2f}  RR: {result['RR']:>6.2f}\n")
    
    # Test 2: ไปข้างหน้า (X เป็นบวก)
    result = kinematics.calculate(linear_x=1.0, linear_y=0.0, angular_z=0.0)
    print("Test 2: Moving Forward (vx=1.0, vy=0, wz=0)")
    print(f"  FL: {result['FL']:>6.2f}  FR: {result['FR']:>6.2f}")
    print(f"  RL: {result['RL']:>6.2f}  RR: {result['RR']:>6.2f}\n")
    
    # Test 3: หันตัว (angular_z เป็นบวก)
    result = kinematics.calculate(linear_x=0.0, linear_y=0.0, angular_z=1.0)
    print("Test 3: Rotating Clockwise (vx=0, vy=0, wz=1.0)")
    print(f"  FL: {result['FL']:>6.2f}  FR: {result['FR']:>6.2f}")
    print(f"  RL: {result['RL']:>6.2f}  RR: {result['RR']:>6.2f}\n")
    
    # Test 4: รวม - ไปข้างหน้า + หันตัว
    result = kinematics.calculate(linear_x=1.0, linear_y=0.0, angular_z=0.5)
    print("Test 4: Forward + Rotate (vx=1.0, vy=0, wz=0.5)")
    print(f"  FL: {result['FL']:>6.2f}  FR: {result['FR']:>6.2f}")
    print(f"  RL: {result['RL']:>6.2f}  RR: {result['RR']:>6.2f}\n")
    
    # Test 5: รวม - ไปข้างหน้า + หันตัว + normalize
    result = kinematics.calculate(linear_x=1.0, linear_y=0.0, angular_z=0.5, normalize=True)
    print("Test 5: Forward + Rotate + Normalize (vx=1.0, vy=0, wz=0.5)")
    print(f"  FL: {result['FL']:>6.2f}  FR: {result['FR']:>6.2f}")
    print(f"  RL: {result['RL']:>6.2f}  RR: {result['RR']:>6.2f}\n")