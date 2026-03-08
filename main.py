# main.py
# ไฟล์หลักสำหรับรัน Demo ทั้งหมดในแล็บนี้
# รันอันนี้อันเดียวเพื่อดูผลลัพธ์ของ asyncio, threading และ multiprocessing

import os
import sys

def run_lab(file_name, title):
    print("\n" + "#" * 50)
    print(f"# {title}")
    print("#" * 50)
    
    # สั่งรันไฟล์ python อื่นๆ
    cmd = f"{sys.executable} \"{file_name}\""
    os.system(cmd)

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("      Python Concurrency Lab (Project)")
    print("=" * 50)

    # รายการไฟล์ที่จะรัน
    labs = [
        ("asyncio_demo.py", "1. เริ่มรัน Asyncio Demo (ช่วยกันทำ)"),
        ("threading_demo.py", "2. เริ่มรัน Threading Demo (ทำหลายอย่างพร้อมกัน)"),
        ("process_pool_demo.py", "3. เริ่มรัน Process Pool Demo (แบ่ง CPU ช่วยกันทำ)"),
    ]

    for lab_file, lab_title in labs:
        run_lab(lab_file, lab_title)

    print("\n" + "=" * 50)
    print("  เสร็จสิ้นการรัน Lab ทั้งหมดแล้วครับ!")
    print("=" * 50)
