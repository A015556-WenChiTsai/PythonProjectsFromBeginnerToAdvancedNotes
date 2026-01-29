import asyncio
import sys

# 1. 定義類別：手動實作非同步上下文管理器協議
class ApiSessionManager:
    def __init__(self, url):
        self.url = url
        self.session_id = None

    # 當進入 async with 區塊時，Python 會自動呼叫這個方法
    async def __aenter__(self):
        print(f"【連線】正在開啟與 {self.url} 的連線...")
        await asyncio.sleep(1)  # 模擬非同步 IO
        self.session_id = "SESSION_888"
        print(f"【準備】連線成功，取得 ID: {self.session_id}")
        return self.session_id  # 這個回傳值會給 'as session'

    # 當離開 async with 區塊時（無論正常結束或出錯），會呼叫這個方法
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"【中斷】正在關閉 {self.url} 的連線...")
        await asyncio.sleep(0.5)
        # 這裡通常用來釋放資源，例如關閉資料庫連線

# 2. 測試主程式
async def main():
    print("--- 開始執行傳統類別 (無裝飾器) 範例 ---")
    
    # 使用方式：async with 類別實例
    async with ApiSessionManager("https://api.example.com") as session:
        print(f"【作業】正在使用 {session} 抓取資料...")
        await asyncio.sleep(0.5)
        print("【作業】資料抓取完成！")
        
    print("--- 範例執行結束 ---")

# 3. 執行邏輯：解決 SyntaxError 與 RuntimeError 的相容寫法
if __name__ == "__main__":
    try:
        # 正常情況下（如 F5 偵錯），使用 asyncio.run 啟動
        asyncio.run(main())
    except RuntimeError:
        # 如果是在 VS Code 互動視窗（Shift+Enter），
        # 因為環境已經在跑 Event Loop，我們改用 create_task 執行。
        # 這樣寫可以避開 'await' 關鍵字出現在函數外導致的 SyntaxError。
        print("！!!!!!!")
        asyncio.create_task(main())