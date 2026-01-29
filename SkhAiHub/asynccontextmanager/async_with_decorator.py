import asyncio
import sys
from contextlib import asynccontextmanager

@asynccontextmanager
async def api_session(url):
    print(f"【連線】正在開啟與 {url} 的連線...")
    await asyncio.sleep(1)
    conn = "SESSION_888"
    try:
        yield conn
    finally:
        print(f"【中斷】正在關閉 {url} 的連線...")
        await asyncio.sleep(0.5)

async def main():
    print("--- 開始執行範例 ---")
    async with api_session("https://api.example.com") as session:
        print(f"【作業】正在使用 {session}...")
        await asyncio.sleep(0.5)
    print("--- 執行結束 ---")

# --- 修改後的執行區塊 ---
if __name__ == "__main__":
    try:
        # 這是標準執行方式 (F5 偵錯會走這裡)
        asyncio.run(main())
    except RuntimeError as e:
        # 如果是在互動式視窗 (Shift+Enter)，因為 Loop 已在運行，asyncio.run 會報錯
        # 我們改用 create_task，這樣就不會用到 'await' 關鍵字，避開 SyntaxError
        if "running event loop" in str(e):
            asyncio.create_task(main())
        else:
            raise e