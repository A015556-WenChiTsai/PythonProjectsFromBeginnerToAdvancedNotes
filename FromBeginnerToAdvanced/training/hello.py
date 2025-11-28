import tkinter as tk

class HelloApp(tk.Tk):
    """
    繼承 tk.Tk，這樣 HelloApp 本身就是一個視窗物件。
    這就像是我們畫了一張「藍圖」，定義這個 App 該長什麼樣子。
    """
    def __init__(self):
        super().__init__()  # 初始化父類別 (tk.Tk)，取得視窗的基本功能
        
        # 設定視窗屬性
        self.title("Hello App")
        self.geometry("300x200")
        
        # 初始化介面元件
        self._create_widgets()

    def _create_widgets(self):
        """
        將建立元件的邏輯獨立出來，讓程式碼更整潔 (關注點分離)。
        """
        self.label = tk.Label(self, text="Hello", font=("Arial", 24))
        self.label.pack(pady=50)

# 這是 Python 的程式進入點保護
# 只有當這個檔案被直接執行時，下面的程式碼才會跑
if __name__ == "__main__":
    app = HelloApp()  # 依照藍圖蓋出房子
    app.mainloop()    # 啟動視窗