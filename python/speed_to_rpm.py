import math

class SpeedToRPM:
    def __init__(self, wheel_radius=0.05):
        """
        :param wheel_radius: รัศมีของล้อหุ่นยนต์ หน่วยเป็นเมตร (เช่น 5 cm = 0.05 m)
        """
        self.wheel_radius = wheel_radius

    def convert(self, linear_speed):
        """
        แปลงความเร็วเชิงเส้น (m/s) เป็นรอบต่อนาที (RPM)
        """
        if self.wheel_radius == 0:
            return 0.0
        
        # คำนวณ RPM ตามสมการฟิสิกส์
        rpm = (linear_speed * 60.0) / (2 * math.pi * self.wheel_radius)
        return round(rpm, 2)  # ปัดทศนิยม 2 ตำแหน่งเพื่อไม่ให้ข้อมูลยาวเกินตอนส่ง

    def format_for_esp32(self, rpm_fl, rpm_fr, rpm_rl, rpm_rr):
        """
        แพ็กข้อมูลเป็น String รูปแบบ <FL,FR,RL,RR> เพื่อส่งให้ ESP32
        """
        return f"<{rpm_fl},{rpm_fr},{rpm_rl},{rpm_rr}>"

# --- ทดสอบการทำงานของไฟล์นี้ ---
if __name__ == "__main__":
    # สมมติว่าล้อรัศมี 48 mm (0.048 m)
    converter = SpeedToRPM(wheel_radius=0.1016)  # 4 นิ้ว = 0.1016 m
    
    # จำลองค่าความเร็วที่ได้มาจาก kinematics.py
    wheel_speeds_m_s = {
        "FL": 1.5,
        "FR": -1.5,
        "RL": 1.5,
        "RR": -1.5
    }
    
    # แปลงแต่ละล้อเป็น RPM
    rpm_fl = converter.convert(wheel_speeds_m_s["FL"])
    rpm_fr = converter.convert(wheel_speeds_m_s["FR"])
    rpm_rl = converter.convert(wheel_speeds_m_s["RL"])
    rpm_rr = converter.convert(wheel_speeds_m_s["RR"])
    
    # แพ็กข้อมูล
    data_packet = converter.format_for_esp32(rpm_fl, rpm_fr, rpm_rl, rpm_rr)
    
    print("--- Speed to RPM Conversion ---")
    print(f"FL: {rpm_fl} RPM")
    print(f"FR: {rpm_fr} RPM")
    print(f"RL: {rpm_rl} RPM")
    print(f"RR: {rpm_rr} RPM")
    print("-" * 31)
    print(f"Data to ESP32 -> {data_packet}")