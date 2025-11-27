import shutil
import schedule
import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

# =================配置區域=================
# 使用 Path 物件，這是現代 Python 處理路徑的標準方式
SOURCE_DIR = Path("/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced")
DESTINATION_DIR = Path("/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/Backups")
LOG_FILE = Path("backup_service.log")

# =================日誌設定=================
def setup_logging():
    """
    設定日誌系統：同時輸出到 Console (終端機) 與 File (檔案)
    使用 RotatingFileHandler 避免日誌檔案無限膨脹
    """
    logger = logging.getLogger("BackupService")
    logger.setLevel(logging.INFO)

    # 格式設定：時間 - 等級 - 訊息
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 1. 檔案處理器 (限制大小為 5MB，保留最近 3 個檔案)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 2. 終端機處理器 (讓你在螢幕上也看得到)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # 加入處理器
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

# 初始化 logger
logger = setup_logging()

# =================核心邏輯=================
def perform_backup(source: Path, dest: Path):
    """
    執行備份邏輯
    :param source: 來源資料夾路徑 (Path object)
    :param dest: 目標根目錄路徑 (Path object)
    """
    # 檢查來源是否存在
    if not source.exists():
        logger.error(f"來源資料夾不存在: {source}")
        return

    # 建立以今天日期為名的目標路徑
    today_str = datetime.now().strftime("%Y-%m-%d")
    target_dir = dest / today_str  # Pathlib 的強大之處，可以用 / 運算符拼接路徑

    logger.info(f"準備開始備份。來源: {source}, 目標: {target_dir}")

    try:
        # 如果目標資料夾已存在，shutil.copytree 預設會報錯
        # 這裡我們先檢查，如果存在則記錄警告並跳過 (或是你可以選擇覆蓋)
        if target_dir.exists():
            logger.warning(f"備份資料夾已存在，跳過本次備份: {target_dir}")
        else:
            shutil.copytree(source, target_dir)
            logger.info(f"備份成功！已儲存至: {target_dir}")
            
    except OSError as e:
        # 捕捉作業系統層級的錯誤 (如權限不足、磁碟空間不足)
        logger.error(f"備份失敗，發生錯誤: {e}")
    except Exception as e:
        # 捕捉其他未預期的錯誤
        logger.critical(f"發生未預期的錯誤: {e}", exc_info=True)

def job():
    """排程任務的包裝函數"""
    logger.info("啟動排程備份任務...")
    perform_backup(SOURCE_DIR, DESTINATION_DIR)

# =================主程式入口=================
if __name__ == "__main__":
    # 1. 確保目標根目錄存在，不存在則建立
    if not DESTINATION_DIR.exists():
        try:
            DESTINATION_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"已建立備份根目錄: {DESTINATION_DIR}")
        except Exception as e:
            logger.critical(f"無法建立備份根目錄: {e}")
            exit(1)

    # 2. 立即執行一次測試
    logger.info("--- 程式啟動，執行首次測試備份 ---")
    perform_backup(SOURCE_DIR, DESTINATION_DIR)

    # 3. 設定排程
    backup_time = "09:48"
    schedule.every().day.at(backup_time).do(job)
    
    logger.info(f"自動備份已排程，將於每天 {backup_time} 執行")
    logger.info("服務運行中... (按 Ctrl+C 結束)")

    # 4. 進入無窮迴圈
    try:
        while True:
            schedule.run_pending()
            time.sleep(60) # 每分鐘檢查一次即可，減少 CPU 消耗
    except KeyboardInterrupt:
        logger.info("使用者手動停止程式 (Ctrl+C)")