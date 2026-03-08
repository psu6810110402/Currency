# Lab: สรุปเรื่อง Python Concurrency

โปรเจกต์นี้เป็นการทดลองเขียน Python เพื่อดูความแตกต่างระหว่าง **Threading**, **asyncio** และ **Process Pool** ครับ

### นายอภิชาติ จะหย่อ

### 6810110402

---

## ไฟล์ต่างๆ ในโปรเจกต์

### 1. `asyncio_demo.py` (ใช้ระบบ Async)

ตัวนี้ลองใช้ระบบ `async` กับ `await` ครับ เหมาะกับงานที่ต้อง "รอ" เยอะๆ เช่น โหลดเว็บ หรือรอฐานข้อมูล

- ใช้ `asyncio.sleep` จำลองการรอ
- ใช้ `asyncio.gather` เพื่อสั่งให้ทุกงานเริ่มรอพร้อมกัน

### 2. `threading_demo.py` (ใช้ระบบ Thread)

ตัวนี้ลองใช้ Thread ครับ เหมาะกับงานที่ต้องโหลดข้อมูลจากเว็บหลายๆ ที่พร้อมกัน

- ใช้ `ThreadPoolExecutor` มาช่วยแชร์งานให้ 5 Thread
- ถ้าไม่ใช้ Thread จะต้องรอโหลดทีละเว็บ เสียเวลามาก

### 3. `process_pool_demo.py` (ใช้ระบบ Multiprocessing)

อันนี้เอาไว้รันงานที่คำนวณหนักๆ (ใช้ CPU เยอะ) เช่น การหาเลขเฉพาะ

- ใช้ `ProcessPoolExecutor` เพื่อดึง CPU ทั้งหมดมาช่วยกันทำงาน
- ถ้าใช้ Thread ธรรมดาจะติดปัญหา GIL ของ Python ทำให้ช้า แต่อันนี้เร็วมาก!

---

## ขั้นตอนการรัน

1. ถ้ารันทีละไฟล์:
   ```bash
   python asyncio_demo.py
   python threading_demo.py
   python process_pool_demo.py
   ```
2. ถ้ารันสรุปทีเดียวทั้งหมด:
   ```bash
   python main.py
   ```

**สรุปสั้นๆ ที่ได้เรียนรู้:**

- อยากให้งาน I/O (รอเน็ต/รอไฟล์) เร็ว -> ใช้ **asyncio** หรือ **threading**
- อยากให้งานคำนวณ (ใช้สูตรคณิตสาสตร์) เร็ว -> ใช้ **multiprocessing**
