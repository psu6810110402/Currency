# process_pool_demo.py
# โปรแกรมคำนวณเลขหนักๆ โดยแบ่งให้แต่ละ CPU ช่วยกันทำ (Parallel)
# ตัวอย่าง: นับจำนวนเฉพาะ (Prime Numbers)

import time
import math
import concurrent.futures
import multiprocessing

# ฟังก์ชันเช็คว่าเลขนี้เป็นเลขเฉพาะไหม
def is_prime_number(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    # ตรวจสอบแค่ถึง Root ของเลขนั้นก็พอ (ประหยัดเวลา)
    limit = int(math.sqrt(n)) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True

# ฟังก์ชันสำหรับนับเลขเฉพาะในช่วงที่กำหนด
def count_primes(start_n, end_n):
    my_pid = multiprocessing.current_process().pid
    start_time = time.perf_counter()
    
    result_count = 0
    for i in range(start_n, end_n):
        if is_prime_number(i):
            result_count += 1
            
    took = time.perf_counter() - start_time
    print(f"  [Process {my_pid}] ช่วง {start_n:,} ถึง {end_n:,} -> เจอ {result_count:,} ตัว (ใช้ {took:.2f} วิ)")
    return result_count

# ฟังก์ชันสำหรับรันงานแบบทีละช่วง (แบบปกติ)
def normal_run(ranges):
    print("\n--- เริ่มรันแบบปกติ (ทีละช่วง) ---")
    start = time.perf_counter()
    all_count = 0
    for r in ranges:
        all_count += count_primes(r[0], r[1])
    total = time.perf_counter() - start
    print(f"แบบปกติใช้เวลารวม: {total:.2f} วินาที | เจอทั้งหมด: {all_count:,}")
    return total

# ฟังก์ชันสำหรับรันงานแบบแบ่ง Process - ใช้ได้หลาย CPU คุ้มค่า!
def pool_run(ranges, num_cpu):
    print(f"\n--- เริ่มรันแบบ Process Pool (ใช้ {num_cpu} CPU) ---")
    start = time.perf_counter()
    
    all_count = 0
    # ใช้ ProcessPoolExecutor เพื่อสั่งงานให้แต่ละ CPU
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cpu) as exec:
        # ต้องใช้ starmap หรือ map แบบส่งค่าไปทำ (ในที่นี้ส่ง range ไป)
        # แต่เพื่อความง่าย ผมรันแยกทีละงานใน pool
        tasks = []
        for r in ranges:
            tasks.append(exec.submit(count_primes, r[0], r[1]))
        
        for t in concurrent.futures.as_completed(tasks):
            all_count += t.result()
            
    total = time.perf_counter() - start
    print(f"แบบใช้ Pool ใช้เวลารวม: {total:.2f} วินาที | เจอทั้งหมด: {all_count:,}")
    return total

if __name__ == "__main__":
    print("=====================================================")
    print("  LAB: ทดลองใช้ Process Pool (CPU-bound tasks)")
    print("=====================================================")

    # กำหนดช่วงที่จะหาเลขเฉพาะ
    START_VAL = 2
    END_VAL = 500000
    
    # ดูว่าคอมเครื่องนี้มีกี่ CPU
    cpu_to_use = 4 
    print(f"จะหาเลขเฉพาะตั้งแต่ {START_VAL:,} ถึง {END_VAL:,}")
    
    # แบ่งช่วงตัวเลขออกเป็นส่วนๆ (4 ส่วนตาม CPU)
    step = (END_VAL - START_VAL) // cpu_to_use
    ranges = []
    for i in range(cpu_to_use):
        s = START_VAL + (i * step)
        e = s + step if i < cpu_to_use - 1 else END_VAL
        ranges.append((s, e))

    t1 = normal_run(ranges)
    t2 = pool_run(ranges, cpu_to_use)

    if t2 > 0:
        print(f"\nสรุป: ใช้ Process Pool เร็วกว่าเดิม {t1/t2:.1f} เท่า!")
    print("เพราะคอมพิวเตอร์สมัยใหม่มีหลาย CPU การใช้ Process Pool ช่วยให้ทำงานขนานกันได้")
