import asyncio
import time

# ---- Simulated async tasks (ไม่ต้องติดตั้ง library พิเศษ) ----

TASKS = [
    {"name": "Task-A", "delay": 1.0, "result": "ผลลัพธ์จาก Task A"},
    {"name": "Task-B", "delay": 0.5, "result": "ผลลัพธ์จาก Task B"},
    {"name": "Task-C", "delay": 1.5, "result": "ผลลัพธ์จาก Task C"},
    {"name": "Task-D", "delay": 0.8, "result": "ผลลัพธ์จาก Task D"},
    {"name": "Task-E", "delay": 0.3, "result": "ผลลัพธ์จาก Task E"},
]


async def simulate_io_task(name: str, delay: float, result: str) -> dict:
    """จำลอง I/O task ที่ต้องรอ (เช่น HTTP request, database query)"""
    start = time.perf_counter()
    print(f"  [asyncio] {name} → เริ่มทำงาน (จะใช้เวลา {delay}s)")
    await asyncio.sleep(delay)  # ส่งคืน control ให้ event loop ระหว่างรอ
    elapsed = time.perf_counter() - start
    print(f"  [asyncio] {name} → เสร็จแล้ว ({elapsed:.2f}s): {result}")
    return {"name": name, "elapsed": elapsed, "result": result}


async def run_sequential_async():
    """รัน tasks ทีละงาน (await ต่อกัน)"""
    print("\n[Asyncio Sequential] รัน tasks ทีละงาน...")
    start = time.perf_counter()
    results = []
    for task in TASKS:
        r = await simulate_io_task(task["name"], task["delay"], task["result"])
        results.append(r)
    total = time.perf_counter() - start
    print(f"[Asyncio Sequential] รวม: {total:.2f}s")
    return total


async def run_concurrent_async():
    """รัน tasks พร้อมกันด้วย asyncio.gather"""
    print("\n[Asyncio Concurrent] รัน tasks พร้อมกันด้วย gather...")
    start = time.perf_counter()
    coroutines = [
        simulate_io_task(t["name"], t["delay"], t["result"]) for t in TASKS
    ]
    results = await asyncio.gather(*coroutines)
    total = time.perf_counter() - start
    print(f"[Asyncio Concurrent] รวม: {total:.2f}s")
    return total


async def run_with_timeout():
    """ตัวอย่างการใช้ timeout กับ async task"""
    print("\n[Asyncio Timeout] ทดสอบ timeout (จำกัด 0.4s)...")
    try:
        result = await asyncio.wait_for(
            simulate_io_task("SlowTask", 2.0, "งานช้า"), timeout=0.4
        )
    except asyncio.TimeoutError:
        print("  [asyncio] SlowTask → หมดเวลา! (TimeoutError)")


async def main():
    print("=" * 55)
    print("  Asyncio Demo: Cooperative Multitasking")
    print("=" * 55)

    seq_time = await run_sequential_async()
    conc_time = await run_concurrent_async()
    await run_with_timeout()

    speedup = seq_time / conc_time if conc_time > 0 else 0
    print(f"\nสรุป: asyncio gather เร็วกว่า {speedup:.1f}x เมื่อเทียบกับ sequential")
    expected_concurrent = max(t["delay"] for t in TASKS)
    print(f"เวลาที่คาดว่าจะใช้ (concurrent): ~{expected_concurrent}s "
          f"(เท่ากับ task ที่นานที่สุด)")


if __name__ == "__main__":
    asyncio.run(main())
