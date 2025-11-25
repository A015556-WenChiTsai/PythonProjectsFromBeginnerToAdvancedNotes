# ⌨️ Python 終端機打字速度測驗 (WPM Test)

這是一個使用 Python 標準庫 `curses` 建立的終端機使用者介面 (TUI) 應用程式，用於測量使用者的打字速度（Words Per Minute, WPM）。

這個專案特別強調了現代 Python 的最佳實踐，包括使用 `pathlib` 進行健壯的檔案管理和全面的錯誤處理。

## 📋 專案結構
.
├── 11_tutorial_v2.py # 核心應用程式 (推薦版本)
├── text.txt # 測驗用的文字內容
└── README.md # 本文件

## 🛠️ 環境要求與安裝

### 1. Python 版本

*   Python 3.6+

### 2. Curses 庫

`curses` 是 Linux/macOS 上的標準庫。但如果您在 **Windows** 環境下執行，您需要安裝一個相容層：

```bash
# 僅限 Windows 使用者
pip install windows-curses