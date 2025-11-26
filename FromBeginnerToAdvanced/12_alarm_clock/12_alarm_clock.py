import tkinter as tk
from tkinter import messagebox
import datetime
import subprocess
import logging
import shutil  # 用來檢查指令是否存在
from pathlib import Path

# --- 1. 設定 Logging ---
# level=logging.DEBUG 代表會顯示所有細節資訊
logging.basicConfig(
    level=logging.DEBUG,  #
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
# %(asctime)s - %(levelname)s - %(message)s
# 看到 %(asctime)s -> 去資料卡找 asctime -> 填入 '12:00:05'
# 看到 %(levelname)s -> 去資料卡找 levelname -> 填入 'ERROR'
# 看到 %(message)s -> 去資料卡找 message -> 填入 '找不到檔案'
# s 代表 String (字串)。
# 它的意思是：「不管抓到什麼資料，請把它轉成文字**印出來。」
# （如果是數字通常用 d，但在 logging 格式設定中，為了保險起見，絕大多數都用 s）。

# 為什麼不用 f-string (f"{...}")？
# 你可能會想，為什麼不寫成：
# format = f"{datetime.now()} - {level} - {msg}" ?
# 原因有兩個：
# 歷史原因：logging 模組出來的時候，Python 還沒有 f-string。
# 效能優化 (Lazy Evaluation)：使用 % 寫法，只有當這條 log 真的需要被印出來時，程式才會去花時間做字串拼接。如果這條 log 被過濾掉（例如等級設為 ERROR 但你只記錄 INFO），程式就不會浪費時間去處理字串，這樣跑得比較快。


class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Debug Alarm Clock")
        self.root.geometry("400x250")

        # 2. 檢查音效檔案路徑
        self.sound_file = Path(__file__).parent / "sound.mp3"
        logging.info(f"程式所在路徑: {Path(__file__).parent}")
        logging.info(f"預期音效路徑: {self.sound_file}")

        if not self.sound_file.exists():
            logging.error(f"❌ 找不到音效檔！請確認 {self.sound_file} 是否存在")
        else:
            logging.info("✅ 音效檔存在")

        # 3. 檢查 mpg123 是否安裝
        if shutil.which("mpg123") is None:
            logging.error(
                "❌ 系統找不到 'mpg123' 指令！請確認是否已安裝 (sudo apt install mpg123)"
            )
        else:
            logging.info(f"✅ 找到 mpg123: {shutil.which('mpg123')}")

        self.is_running = False
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(
            self.root, text="Debug Mode Alarm", font=("Helvetica", 12, "bold")
        ).pack(pady=10)
        # pack(pady=10):幫我留一點空隙（10單位）

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        # 預設填入當前時間，方便測試
        now = datetime.datetime.now()
        self.hour_var = tk.StringVar(value=now.strftime("%H"))
        #tk.StringVar：這是 Tkinter 專用的變數類型。
        # now.strftime("%H")：把現在時間 (now) 的小時抓出來，轉成兩位數的字串（例如 "14"）
        # now.strftime("%M")：把現在時間的分鐘抓出來（例如 "30"）。
        self.min_var = tk.StringVar(value=now.strftime("%M"))
        # 預設秒數 + 5 秒 (方便你測試)
        future_sec = (now.second + 5) % 60
        self.sec_var = tk.StringVar(value=f"{future_sec:02d}")

        entry_opts = {
            "width": 5,
            "font": ("Arial", 12),
            "justify": "center",
            "bg": "pink",
        }
        tk.Entry(input_frame, textvariable=self.hour_var, **entry_opts).pack(
            side=tk.LEFT, padx=5
        )
        tk.Entry(input_frame, textvariable=self.min_var, **entry_opts).pack(
            side=tk.LEFT, padx=5
        )
        tk.Entry(input_frame, textvariable=self.sec_var, **entry_opts).pack(
            side=tk.LEFT, padx=5
        )

        self.btn_set = tk.Button(
            self.root, text="Set Alarm", fg="red", command=self.start_alarm
        )
        self.btn_set.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Ready", font=("Arial", 10))
        self.status_label.pack()

    def start_alarm(self):
        h = self.hour_var.get().zfill(2)
        m = self.min_var.get().zfill(2)
        s = self.sec_var.get().zfill(2)
        # .zfill(2)  # 不足兩位補零

        self.target_time = f"{h}:{m}:{s}"
        self.is_running = True

        logging.info(f"🔔 鬧鐘已設定，目標時間: {self.target_time}")
        self.status_label.config(text=f"Waiting for {self.target_time}...")
        self.btn_set.config(state="disabled")

        self.check_time()

    def check_time(self):
        if not self.is_running:
            return

        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # 4. 記錄比對過程 (Debug 等級)
        # 如果覺得太吵，可以把這行註解掉，但這是除錯關鍵
        logging.debug(f"比對中... 現在: {current_time} vs 目標: {self.target_time}")

        if current_time == self.target_time:
            logging.info("⏰ 時間到！準備播放聲音...")
            self.play_sound()
            self.is_running = False
            self.status_label.config(text="WAKE UP!")
            self.btn_set.config(state="normal")
        else:
            # 500ms 檢查一次，比 1000ms 更精準，避免剛好跳過
            self.root.after(500, self.check_time)

    def play_sound(self):
        if not self.sound_file.exists():
            logging.error("❌ 播放失敗：找不到檔案")
            messagebox.showerror("Error", "Sound file missing!")
            return

        cmd = ["mpg123", "-q", str(self.sound_file)]
        logging.info(f"▶️ 執行指令: {' '.join(cmd)}")

        try:
            # 使用 Popen 執行
            proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 如果你想確認是否有錯誤輸出，可以稍後檢查 proc.communicate()
            logging.info("✅ 指令已發送")
        except FileNotFoundError:
            logging.critical("❌ 嚴重錯誤：系統找不到 mpg123，請確認已安裝")
            messagebox.showerror("Error", "mpg123 not installed")
        except Exception as e:
            logging.error(f"❌ 未知錯誤: {e}")


if __name__ == "__main__":
    root = (
        tk.Tk()
    )  # 1. 建立主視窗 (畫布)【啟動 GUI「圖形使用者介面」 程式並建立第一個視窗】
    app = AlarmClockApp(root)  # 2. 把這個畫布傳給你的 App 類別去佈置 (放按鈕、放標籤)
    root.mainloop()  # 3. 啟動視窗循環，讓程式保持執行
