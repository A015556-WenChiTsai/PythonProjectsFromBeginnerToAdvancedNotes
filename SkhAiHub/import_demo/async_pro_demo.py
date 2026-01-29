import asyncio
import time
from contextlib import asynccontextmanager

# ==========================================
# 第一部分：定義工具 (這部分被 import 時不會自動執行)
# ==========================================

@asynccontextmanager
async def time_it(label):
    """這是一個計時工具，就像一個碼錶"""
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"【計時】{label} 耗時: {end - start:.4f} 秒")

async def main_demo():
    """這是我們的測試示範邏輯"""
    print("--- 正在執行示範程式 ---")
    async with time_it("模擬工作"):
        await asyncio.sleep(1)
    print("--- 示範結束 ---")

# ==========================================
# 第二部分：關鍵的「閘門」 (if __name__ == "__main__")
# ==========================================

# 這裡就像是一個開關：
# 1. 如果你「直接執行」這個檔案，__name__ 就會是 "__main__"，下面的代碼會跑。
# 2. 如果別人「import」這個檔案，__name__ 就不是 "__main__"，下面的代碼會「自動閉嘴」。

if __name__ == "__main__":
    # 這裡放的是「只有當你是主角時」才要做的事
    print(f"目前的身份是: {__name__} (我是主角，我要執行測試！)")
    
    try:
        # 這是啟動非同步程式的標準做法
        asyncio.run(main_demo())
    except RuntimeError:
        # 這是為了相容 VS Code / Jupyter 的特殊處理
        loop = asyncio.get_event_loop()
        loop.create_task(main_demo())
else:
    # 這裡通常不寫東西，我寫這行是為了讓你理解
    print(f"目前的身份是: {__name__} (我被別人引用了，我會安靜地提供工具)")