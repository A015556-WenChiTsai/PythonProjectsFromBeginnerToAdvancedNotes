import logging
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin

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
# 2. 常數定義 (Constants)
# ==========================================
BASE_URL = "https://data.nba.net"
ENDPOINT_TODAY = "/prod/v1/today.json"

# ==========================================
# 3. 工具函式 (Helper Functions)
# ==========================================
def fetch_json(session: requests.Session, url: str) -> Dict[str, Any]:
    """
    通用的 JSON 抓取函式，包含錯誤處理。
    """
    logger.debug(f"正在請求 URL: {url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"請求失敗: {url} | 錯誤: {e}")
        return {}

def get_links(session: requests.Session) -> Dict[str, str]:
    """取得 NBA API 的導航連結"""
    url = urljoin(BASE_URL, ENDPOINT_TODAY)
    data = fetch_json(session, url)
    
    links = data.get('links', {})
    logger.debug(f"取得 Links 數量: {len(links)}")
    return links

# ==========================================
# 4. 核心邏輯
# ==========================================
def print_scoreboard(session: requests.Session) -> None:
    """取得並顯示記分板"""
    logger.info(">>> 開始執行: 記分板查詢")
    
    links = get_links(session)
    if not (endpoint := links.get('currentScoreboard')): # Python 3.8+ 海象運算子 (Walrus Operator)
        logger.warning("找不到 currentScoreboard 連結")
        return

    url = urljoin(BASE_URL, endpoint)
    data = fetch_json(session, url)
    games = data.get('games', [])

    logger.info(f"今日賽事總數: {len(games)}")

    for game in games:
        # 使用 .get() 避免 KeyError，並設定預設值
        h_team = game.get('hTeam', {})
        v_team = game.get('vTeam', {})
        period = game.get('period', {})
        
        # 格式化輸出
        print("-" * 40)
        print(f"{h_team.get('triCode')} vs {v_team.get('triCode')}")
        print(f"{h_team.get('score')} - {v_team.get('score')}")
        print(f"{game.get('clock')} - {period.get('current')}")

def print_stats(session: requests.Session) -> None:
    """取得並顯示球隊數據排名"""
    logger.info(">>> 開始執行: 數據排名查詢")

    links = get_links(session)
    if not (endpoint := links.get('leagueTeamStatsLeaders')):
        logger.warning("找不到 leagueTeamStatsLeaders 連結")
        return

    url = urljoin(BASE_URL, endpoint)
    data = fetch_json(session, url)
    
    # 安全地深入取得巢狀資料
    try:
        teams: List[Dict] = data['league']['standard']['regularSeason']['teams']
    except KeyError:
        logger.error("JSON 結構改變，無法找到 teams 資料")
        return

    logger.debug(f"原始隊伍數量: {len(teams)}")

    # -------------------------------------------------------
    # Pythonic 重點：List Comprehension (列表推導式)
    # 取代原本的 filter(lambda...)
    # -------------------------------------------------------
    valid_teams = [
        team for team in teams 
        if team.get('name') != "Team"
    ]
    logger.debug(f"有效隊伍數量: {len(valid_teams)}")

    # 排序：使用 lambda 提取排序鍵值
    # 這裡加上 try-except 保護，防止 rank 不是數字時報錯
    try:
        valid_teams.sort(key=lambda x: int(x.get('ppg', {}).get('rank', 999)))
    except ValueError as e:
        logger.error(f"排序時發生錯誤 (資料格式問題): {e}")

    # 顯示結果
    for i, team in enumerate(valid_teams, start=1):
        name = team.get('name', 'Unknown')
        nickname = team.get('nickname', '')
        ppg = team.get('ppg', {}).get('avg', 'N/A')
        
        logger.debug(f"Rank {i}: {name} ({ppg} PPG)")
        print(f"{i}. {name} - {nickname} - {ppg}")

# ==========================================
# 5. 程式進入點 (Entry Point)
# ==========================================
if __name__ == "__main__":
    # 使用 Session Context Manager，自動處理連線關閉
    with requests.Session() as session:
        # 設定 User-Agent 讓爬蟲看起來像瀏覽器 (這是爬蟲的基本禮貌)
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Python NBA Client)"
        })
        
        # 執行功能
        print_stats(session)
        # print_scoreboard(session)