import asyncio
import time
import sys
from contextlib import asynccontextmanager

# ==========================================
# 場景 1：API 連線管理 (確保資源釋放)
# ==========================================

# --- 有使用 @asynccontextmanager ---
@asynccontextmanager
async def api_session(name):
    print(f"【有】開啟 {name} 連線")
    yield f"Session({name})"
    print(f"【有】關閉 {name} 連線")

# --- 沒有使用 (手動處理) ---
async def run_scenario_1():
    print("\n>>> 場景 1: API 連線")
    
    # 有裝飾器：優雅、自動關閉
    async with api_session("Google") as s:
        print(f"  使用中: {s}")

    # 沒有裝飾器：你必須手動寫 try...finally，否則出錯時連線不會關閉
    print("  (手動模式開始)")
    # 模擬手動開啟
    s_manual = f"Session(Manual)"
    print(f"  【無】開啟 {s_manual}")
    try:
        print(f"  使用中: {s_manual}")
    finally:
        print(f"  【無】關閉 {s_manual}")

# ==========================================
# 場景 2：資料庫事務 (Transaction)
# ==========================================

@asynccontextmanager
async def transaction(db_name):
    print(f"【有】SQL: BEGIN TRANSACTION ON {db_name}")
    try:
        yield f"TX_{db_name}"
        print(f"【有】SQL: COMMIT")
    except Exception as e:
        print(f"【有】SQL: ROLLBACK (因為 {e})")
        raise

async def run_scenario_2():
    print("\n>>> 場景 2: 資料庫事務")
    
    # 有裝飾器：自動判斷 Commit 或 Rollback
    try:
        async with transaction("UserDB") as tx:
            print(f"  執行轉帳操作... {tx}")
            # raise ValueError("餘額不足！") # 拿掉註解可測試自動 Rollback
    except: pass

    # 沒有裝飾器：每個轉帳的地方都要寫這一大堆
    print("  (手動模式開始)")
    print("  【無】SQL: BEGIN")
    try:
        print("  執行轉帳操作...")
        print("  【無】SQL: COMMIT")
    except:
        print("  【無】SQL: ROLLBACK")

# ==========================================
# 場景 3：效能計時器 (Profiling)
# ==========================================

@asynccontextmanager
async def time_it(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"【計時】{label} 耗時: {end - start:.4f} 秒")

async def run_scenario_3():
    print("\n>>> 場景 3: 效能計時")
    
    # 有裝飾器：只要一行包住
    async with time_it("下載圖片"):
        await asyncio.sleep(0.5)

    # 沒有裝飾器：你得在每個要計時的地方手動算時間
    print("  (手動模式開始)")
    t0 = time.perf_counter()
    await asyncio.sleep(0.5)
    t1 = time.perf_counter()
    print(f"  【無】手動計時: {t1 - t0:.4f} 秒")

# ==========================================
# 場景 4：暫時修改全域配置 (Config)
# ==========================================

app_config = {"debug": False}

@asynccontextmanager
async def debug_mode():
    old_state = app_config["debug"]
    app_config["debug"] = True
    print(f"【有】Debug 模式已開啟")
    try:
        yield
    finally:
        app_config["debug"] = old_state
        print(f"【有】Debug 模式已還原為 {old_state}")

async def run_scenario_4():
    print("\n>>> 場景 4: 暫時配置")
    
    # 有裝飾器：確保執行完後配置一定會還原
    async with debug_mode():
        print(f"  當前配置: {app_config}")

    # 沒有裝飾器：如果中間程式碼報錯，你的系統就會一直停在 Debug 模式，很危險
    print("  (手動模式開始)")
    app_config["debug"] = True
    print("  執行某些測試...")
    app_config["debug"] = False # 萬一上面報錯，這行就不會執行！
    print(f"  當前配置: {app_config}")

# ==========================================
# 執行所有場景
# ==========================================
async def main():
    await run_scenario_1()
    await run_scenario_2()
    await run_scenario_3()
    await run_scenario_4()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        asyncio.create_task(main())