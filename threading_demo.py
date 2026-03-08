# threading_demo.py
# โปรแกรมจำลองการโหลดข้อมูลจากหลายเว็บพร้อมกันโดยใช้ Thread
# Thread จะช่วยให้เราไม่ต้องรอโหลดทีละเว็บ

import time
import threading
import concurrent.futures
import urllib.request

# เว็บที่จะลองโหลด (ใช้ delay ของ httpbin เพื่อจำลองการรอเน็ต)
URL_LIST = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/uuid",
    "https://httpbin.org/uuid",
]

# ฟังก์ชันดึงข้อมูลจากเว็บ
def get_data_from_web(url):
    # ชื่อของ thread ที่กำลังทำงานอยู่
    my_name = threading.current_thread().name
    start = time.perf_counter()
    
    try:
        # ลองเปิดเว็บและอ่านข้อมูล
        with urllib.request.urlopen(url, timeout=10) as res:
            data = res.read()
            took = time.perf_counter() - start
            print(f"  [{my_name}] โหลด {url} สำเร็จ! ({len(data)} ไบต์, ใช้ {took:.2f} วิ)")
            return True
    except:
        # ถ้าโหลดไม่ได้ (เช่น เน็ตหลุด หรือ timeout)
        print(f"  [{my_name}] โหลด {url} ไม่สำเร็จ T_T")
        return False

# แบบรันทีละอัน (ต่อคิว) - ช้าแน่นอน
def run_normal():
    print("\n--- เริ่มโหลดแบบปกติ (ทีละเว็บ) ---")
    start = time.perf_counter()
    
    results = []
    for u in URL_LIST:
        results.append(get_data_from_web(u))
        
    total = time.perf_counter() - start
    print(f"แบบปกติใช้เวลารวม: {total:.2f} วินาที")
    return total

# แบบใช้ Thread Pool - เร็วเพราะทำงานพร้อมกัน
def run_with_thread():
    print("\n--- เริ่มโหลดแบบใช้ Thread Pool (พร้อมกัน) ---")
    start = time.perf_counter()
    
    # สร้าง Thread มา 5 ตัวช่วยกันทำงาน
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as worker:
        # สั่งให้ worker ทุกตัวไปรันฟังก์ชัน get_data_from_web ตามรายการ URL
        worker.map(get_data_from_web, URL_LIST)
        
    total = time.perf_counter() - start
    print(f"แบบใช้ Thread ใช้เวลารวม: {total:.2f} วินาที")
    return total

if __name__ == "__main__":
    print("=====================================================")
    print("  LAB: ทดลองใช้ Threading (I/O-bound tasks)")
    print("=====================================================")

    t1 = run_normal()
    t2 = run_with_thread()

    if t2 > 0:
        print(f"\nสรุป: ใช้ Thread เร็วกว่าแบบปกติ {t1/t2:.1f} เท่า!")
    print("เพราะ Thread ช่วยให้เราไม่ต้องรอโหลดทีละเว็บให้เสร็จ")
