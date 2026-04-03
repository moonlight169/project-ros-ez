from pynput import keyboard

# เก็บค่า cmd_vel ปัจจุบัน
cmd_vel = {
    "linear_x": 0.0,   # เดินหน้า/ถอยหลัง
    "linear_y": 0.0,   # สไลด์ซ้าย/ขวา (Mecanum)
    "angular_z": 0.0   # หมุนตัวซ้าย/ขวา
}

SPEED_STEP = 0.5
TURN_STEP = 0.5

def print_status():
    """แสดงผลค่า cmd_vel ทั้ง 3 แกน"""
    print(f"X (F/B): {cmd_vel['linear_x']:>5.1f} | Y (L/R): {cmd_vel['linear_y']:>5.1f} | Z (Turn): {cmd_vel['angular_z']:>5.1f}")

def on_press(key):
    global cmd_vel
    
    # ดักจับการกด Ctrl + C (ตัวอักษรพิเศษรหัส '\x03') เพื่อออกจากโปรแกรม
    if hasattr(key, 'char') and key.char == '\x03':
        print("\nExiting program...")
        return False # คืนค่า False เพื่อหยุด Listener
        
    try:
        char = key.char.lower()
        
        # ==========================================
        # เดินหน้า / ถอยหลัง (Linear X)
        # ==========================================
        if char in ['w', 'i']:
            cmd_vel["linear_x"] += SPEED_STEP
        elif char in ['x', ',']:    # เปลี่ยนจาก 's' เป็น 'x' เพื่อถอยหลัง
            cmd_vel["linear_x"] -= SPEED_STEP
            
        # ==========================================
        # หมุนตัวซ้าย / หมุนตัวขวา (Angular Z)
        # ==========================================
        elif char == 'a':
            cmd_vel["angular_z"] += TURN_STEP
        elif char == 'd':
            cmd_vel["angular_z"] -= TURN_STEP
            
        # ==========================================
        # สไลด์ซ้าย / สไลด์ขวา (Linear Y)
        # ==========================================
        elif char == 'j':
            cmd_vel["linear_y"] += SPEED_STEP
        elif char == 'l':
            cmd_vel["linear_y"] -= SPEED_STEP
            
        # ==========================================
        # การเคลื่อนที่แบบเข้าโค้ง (Arc Movement)
        # ==========================================
        elif char == 'u':
            cmd_vel["linear_x"] += SPEED_STEP
            cmd_vel["angular_z"] += TURN_STEP
        elif char == 'o':
            cmd_vel["linear_x"] += SPEED_STEP
            cmd_vel["angular_z"] -= TURN_STEP
        elif char == 'm':
            cmd_vel["linear_x"] -= SPEED_STEP
            cmd_vel["angular_z"] += TURN_STEP
        elif char == '.':
            cmd_vel["linear_x"] -= SPEED_STEP
            cmd_vel["angular_z"] -= TURN_STEP
            
        # ==========================================
        # หยุดการเคลื่อนที่ (Stop)
        # ==========================================
        elif char in ['s', 'k']:    # เปลี่ยนจาก 'x' เป็น 's' เพื่อหยุดรถ
            cmd_vel["linear_x"] = 0.0
            cmd_vel["linear_y"] = 0.0
            cmd_vel["angular_z"] = 0.0
            
        print_status()

    except AttributeError:
        pass

def on_release(key):
    pass

def starts_ui():
     # --- UI เริ่มต้น ---
    print("--- Ultimate Mecanum Controller (Custom Mapping) ---")
    print(" [Left Hand]                [Right Hand]              ")
    print("            W                     U    I    O         ")
    print("          A S D                   J    K    L         ")
    print("            X                     M    ,    .         ")
    print("------------------------------------------------------")
    print(" W/X : Forward/Backward     U/O : Curve Forward       ")
    print(" A/D : Turn Left/Right      M/. : Curve Backward      ")
    print(" S/K : STOP                 J/L : Strafe Left/Right   ")
    print("                            I/, : Forward/Backward    ")
    print("------------------------------------------------------")
    print(" Ctrl+C : Exit Program")
    print("------------------------------------------------------")
    
def main():
    starts_ui()
    print_status()

    try:
        # เปิดตัวดักจับอีเวนต์คีย์บอร์ด
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\nExiting program...")

if __name__ == "__main__":
   main()