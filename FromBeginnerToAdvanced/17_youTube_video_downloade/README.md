# YouTube Video Downloader (Enterprise Logging Edition)

這是一個基於 Python 的 YouTube 影片下載工具。
它不僅僅是一個下載腳本，更是一個展示 **Python 最佳實踐 (Best Practices)** 的教學範例，特別著重於 **日誌管理 (Logging)** 與 **現代化路徑處理**。

## 🚀 功能特色 (Features)

*   **高品質下載**：使用強大的 `yt-dlp` 核心，自動選擇最佳畫質與音質。
*   **企業級日誌系統 (Advanced Logging)**：
    *   **雙重輸出**：終端機顯示簡潔資訊 (INFO)，Log 檔案記錄詳細除錯資訊 (DEBUG)。
    *   **自動輪替**：Log 檔案按天切割，自動清理舊檔案，避免佔用硬碟空間。
*   **圖形化路徑選擇**：整合 `tkinter` 彈出視窗，讓使用者直觀選擇儲存資料夾。
*   **健壯的錯誤處理**：發生錯誤時會記錄完整的堆疊追蹤 (Traceback) 至檔案。
*   **現代化語法**：全面使用 Type Hinting (型別提示) 與 `pathlib`。

## 🛠️ 安裝需求 (Prerequisites)

在執行此程式之前，請確保您已安裝 Python 3.6+ 以及以下套件：

1.  **安裝 Python 套件**：
    ```bash
    pip install yt-dlp
    ```
    *(註：`tkinter` 通常內建於 Python 安裝中，無需額外安裝)*

2.  **安裝 FFmpeg (強烈建議)**：
    為了讓 `yt-dlp` 能順利合併高畫質視訊與音訊，電腦需安裝 FFmpeg。
    *   **Windows**: 下載 FFmpeg 執行檔並設定環境變數。
    *   **Mac**: `brew install ffmpeg`
    *   **Linux**: `sudo apt install ffmpeg`

## 📖 程式碼學習重點 (Code Analysis)

對於初學者，這段程式碼有幾個值得深入研究的技術點：

### 1. Logging 設定 (`setup_logging`)
這段程式碼示範了如何設定專業的 Log：
```python
# 每天切割 Log，保留 7 天，支援中文
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='youtube_downloader.log', 
    when='D', interval=1, backupCount=7, encoding='utf-8'
)