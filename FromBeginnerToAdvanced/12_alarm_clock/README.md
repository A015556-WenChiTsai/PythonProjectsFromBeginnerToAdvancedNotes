# ⏰ Python Debug Alarm Clock (Python 除錯鬧鐘)

這是一個適合 Python 初學者學習 **GUI 開發**、**日誌系統 (Logging)** 與 **外部程序呼叫 (Subprocess)** 的教學範例專案。

它不僅僅是一個鬧鐘，更展示了如何編寫具備「防禦性程式設計」思維的程式碼。

## 📚 你將從這個專案學到什麼？

1.  **Tkinter GUI 基礎**：建立視窗、輸入框、按鈕，以及如何更新介面文字。
2.  **Logging 日誌系統**：取代 `print()`，使用專業的格式記錄程式運行狀態與錯誤。
3.  **Pathlib 路徑處理**：現代化的檔案路徑操作，確保跨平台相容性。
4.  **Subprocess 外部呼叫**：如何在 Python 中執行系統指令（如播放音效）。
5.  **非阻塞式迴圈**：使用 `root.after()` 實現定時檢查，避免視窗卡死。

## 🛠️ 系統需求 (Prerequisites)

在執行此程式之前，請確保您的環境已安裝以下工具：

### 1. Python
*   建議版本：Python 3.8 或以上

### 2. 外部播放器 (mpg123)
本程式依賴 `mpg123` 來播放 MP3 音效。

*   **Ubuntu/Debian Linux:**
    ```bash
    sudo apt-get install mpg123
    ```
*   **macOS (使用 Homebrew):**
    ```bash
    brew install mpg123
    ```
*   **Windows:**
    需下載 mpg123 執行檔並設定環境變數，或修改程式碼改用 `winsound` 或 `playsound` 函式庫。

### 3. 音效檔案
請在程式碼的同一層目錄下，放入一個名為 `sound.mp3` 的檔案。

## 🚀 如何執行 (How to Run)

1.  確保 `sound.mp3` 已經在資料夾中。
2.  執行 Python 腳本：
    ```bash
    python alarm_clock.py
    ```
3.  視窗開啟後，程式會自動填入「當前時間 + 5秒」。
4.  點擊 **Set Alarm** 按鈕。
5.  觀察終端機 (Terminal) 的 Log 輸出，等待時間到達。

## 🔍 程式碼結構解析

### Logging 設定
```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    ...
)