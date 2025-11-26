import logging
import logging.handlers  # 引入 handlers 模組
import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional
import yt_dlp

# ==========================================
# 企業級 Logging 設定區
# ==========================================
def setup_logging():
    # 1. 建立 Logger 物件
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) # 總開關設為 DEBUG，具體過濾交給 Handler

    # 設定 Log 格式
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # ------------------------------------------
    # Handler A: 寫入檔案 (包含 Log Rotation)
    # ------------------------------------------
    # 檔名: app.log
    # when='D': 每天 (Day) 切割一次
    # interval=1: 每 1 天
    # backupCount=7: 只保留最近 7 個檔案 (第 8 個會被自動刪除)
    # encoding='utf-8': 支援中文
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='youtube_downloader.log', 
        when='D', 
        interval=1, 
        backupCount=7, 
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG) # 檔案裡記錄最詳細的 DEBUG 資訊
    file_handler.setFormatter(formatter)
    
    # ------------------------------------------
    # Handler B: 輸出到螢幕 (Console)
    # ------------------------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # 螢幕只顯示 INFO，保持乾淨
    console_handler.setFormatter(formatter)

    # 將兩個 Handler 加入 Logger
    # 避免重複添加 (Jupyter 或重複執行時常發生)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

# 初始化 Logging
setup_logging()

# ==========================================
# 主程式邏輯
# ==========================================

def my_hook(d):
    """yt-dlp 進度回調"""
    if d['status'] == 'finished':
        logging.info('檔案下載完成，正在進行轉檔或合併...')
    elif d['status'] == 'downloading':
        # 這裡用 debug，所以只會寫入檔案，不會在螢幕洗版！
        logging.debug(f"下載進度: {d.get('_percent_str', 'N/A')}")

def download_video(url: str, save_path: Path) -> None:
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(save_path / '%(title)s.%(ext)s'),
        'logger': logging.getLogger(), # 讓 yt-dlp 的 log 也進入我們的系統
        'progress_hooks': [my_hook],
    }

    try:
        logging.info(f"正在解析影片 URL: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            logging.info(f"影片標題: {video_title}")
            logging.info(f"開始下載至: {save_path}")
            
            ydl.download([url])
            
        logging.info("下載成功！ (Video downloaded successfully)")

    except Exception as e:
        # exc_info=True 會把完整的錯誤堆疊 (Traceback) 寫入檔案，方便除錯
        logging.error(f"下載過程中發生錯誤: {e}", exc_info=True)

def select_directory() -> Optional[Path]:
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory()
    root.destroy()

    if folder_selected:
        path_obj = Path(folder_selected)
        logging.info(f"使用者選擇了資料夾: {path_obj}")
        return path_obj
    
    logging.warning("使用者取消了資料夾選擇。")
    return None

def main():
    video_url = input("Please enter a YouTube url: ").strip()
    if not video_url:
        logging.error("未輸入 URL，程式結束。")
        return

    save_dir = select_directory()

    if save_dir:
        download_video(video_url, save_dir)
    else:
        logging.info("因未選擇儲存路徑，取消下載。")

if __name__ == "__main__":
    main()