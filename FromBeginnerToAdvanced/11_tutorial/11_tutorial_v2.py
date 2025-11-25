import curses
from curses import wrapper
import time
import random
from pathlib import Path # 引入 pathlib 模組


def start_screen(stdscr):
    """顯示歡迎畫面並等待使用者按鍵開始"""
    stdscr.clear()
    stdscr.addstr("歡迎參加打字速度測驗！")
    stdscr.addstr("\n按任意鍵開始！")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    """在螢幕上顯示目標文字、使用者輸入和 WPM"""
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) # 綠色 (正確)
        if char != correct_char:
            color = curses.color_pair(2) # 紅色 (錯誤)

        # 在 (0, i) 位置顯示輸入的字元，並應用顏色
        stdscr.addstr(0, i, char, color)

def load_text():
    """
    使用 pathlib 載入 text.txt 中的隨機一行文字。
    """
    
    # 獲取當前腳本所在的目錄，並將檔名替換為 "text.txt"
    file_path = Path(__file__).with_name("text.txt")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                raise ValueError(f"File {file_path} is empty.")
            
            # 確保 return 語句正確縮排
            return random.choice(lines).strip()
    
    # 確保 except 語句與 try 語句對齊
    except FileNotFoundError:
        # 如果檔案真的不存在，提供更清晰的錯誤訊息
        raise FileNotFoundError(f"Could not find text file at expected path: {file_path}")


def wpm_test(stdscr):
    """執行實際的打字測試邏輯"""
    try:
        target_text = load_text()
    except (FileNotFoundError, ValueError) as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error loading text: {e}")
        stdscr.addstr(1, 0, "Press any key to exit.")
        stdscr.refresh()
        stdscr.getkey()
        return

    current_text = []
    wpm = 0
    start_time = time.time()
    
    # 設置 nodelay=True 讓 getkey() 不阻塞，以便計算 WPM
    stdscr.nodelay(True) 

    # 確保 while True 縮排正確
    while True:
        # 計算 WPM
        time_elapsed = max(time.time() - start_time, 1) # 確保時間不為零
        # WPM 公式: (字元數 / 5) / (時間(秒) / 60)
        wpm = round((len(current_text) / 5) / (time_elapsed / 60))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # 檢查是否完成
        if "".join(current_text) == target_text:
            stdscr.nodelay(False) # 完成後恢復阻塞模式，等待使用者按鍵
            break

        try:
            key = stdscr.getkey()
        except:
            # 如果沒有按鍵，則繼續迴圈 (因為 nodelay=True)
            continue

        # 退出鍵 (ESC)
        if ord(key) == 27:
            break

        # 處理退格鍵
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        # 處理一般輸入
        elif len(current_text) < len(target_text) and len(key) == 1:
            current_text.append(key)


def main(stdscr):
    """主函式：初始化 curses 顏色並控制流程"""
    
    # 初始化顏色對 (Color Pairs)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        
        # 測試結束畫面
        stdscr.addstr(2, 0, "文字輸入完畢！按任意鍵繼續，或按 ESC 鍵退出。")
        stdscr.refresh()
        
        # 使用 getch() 替代 getkey()
        key_code = stdscr.getch() 
        
        # 27 是 ESC 鍵的 ASCII 碼
        if key_code == 27: 
            break

# 啟動 curses 應用
if __name__ == "__main__":
    wrapper(main)