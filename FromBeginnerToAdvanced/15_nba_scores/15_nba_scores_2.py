import logging
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin
import json 
import requests
from requests import RequestException

# ==========================================
# 1. 設定 Logging
# ==========================================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. 常數定義 (改用 JSONPlaceholder)
# ==========================================
BASE_URL = "https://jsonplaceholder.typicode.com"
ENDPOINT_USERS = "/users"

# ==========================================
# 3. 工具函式
# ==========================================
def fetch_json(session: requests.Session, url: str) -> Any:
    """通用的 JSON 抓取函式"""
    logger.debug(f"正在請求 URL: {url}")
    try:
        # verify=True 是預設值，但在某些公司內網可能需要設為 False (這裡保持預設)
        response = session.get(url, timeout=10)
        logger.info(f"response 1: {response}")
        response.raise_for_status()
        logger.info(f"response 2: {response}")
        return response.json()
    except RequestException as e:
        logger.error(f"請求失敗: {url} | 錯誤: {e}")
        return []

# ==========================================
# 4. 核心邏輯 (改寫為處理 Users)
# ==========================================
def print_user_stats(session: requests.Session) -> None:
    """取得並顯示使用者資料"""
    logger.info(">>> 開始執行: 使用者資料查詢")

    url = urljoin(BASE_URL, ENDPOINT_USERS)
    # 這裡回傳的直接是一個 List，不是字典
    users: List[Dict] = fetch_json(session, url)
    # logger.info(f"users: {users}")
    logger.info(f"users: \n{json.dumps(users, indent=4, ensure_ascii=False)}")
    if not users:
        logger.warning("沒有取得任何使用者資料")
        return

    logger.debug(f"原始使用者數量: {len(users)}")

    # -------------------------------------------------------
    # 練習 1: 過濾 (Filtering)
    # 模擬情境：我們只想要 ID 小於等於 5 的資深員工
    # -------------------------------------------------------
    valid_users = [
        user for user in users 
        if user.get('id', 999) <= 5
    ]
    logger.debug(f"過濾後使用者數量 (ID <= 5): {len(valid_users)}")

    # -------------------------------------------------------
    # 練習 2: 排序 (Sorting)
    # 模擬情境：依照 username 的字母順序排序
    # -------------------------------------------------------
    try:
        valid_users.sort(key=lambda x: x.get('username', ''))
        logger.debug("使用者已按 Username 排序完成")
    except Exception as e:
        logger.error(f"排序時發生錯誤: {e}")

    # -------------------------------------------------------
    # 顯示結果
    # -------------------------------------------------------
    print("\n" + "="*40)
    print(f"{'ID':<5} | {'Name':<20} | {'Username':<15}")
    print("-" * 40)
    
    for user in valid_users:
        uid = user.get('id')
        name = user.get('name')
        username = user.get('username')
        
        # Log 詳細資料
        logger.debug(f"Processing: {name} ({username})")
        
        # 格式化輸出
        print(f"{uid:<5} | {name:<20} | {username:<15}")
    print("="*40 + "\n")

# ==========================================
# 5. 程式進入點
# ==========================================
if __name__ == "__main__":
    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "Python Learning Client"
        })
        #「開啟一個高效能的連續通話模式 (Session)，並保證結束後自動掛斷 (with)。在通話開始前，先設定好我的假身分證 (User-Agent)，讓伺服器以為我是合法的訪客，而不是隨便寫的腳本。」
        
        print_user_stats(session)