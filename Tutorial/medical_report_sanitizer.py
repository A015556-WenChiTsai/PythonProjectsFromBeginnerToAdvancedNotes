import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
import platform

# --- 核心邏輯區 (不變) ---
def core_deidentify_logic(report_content: str) -> str:
    patterns = [
        r".{2,3}醫師\(放診專", r"姓名", r"病歷號", r"醫囑醫師",
        r"新光吳火獅紀念醫院", r"病患姓名"
    ]
    ignore_pattern = re.compile("|".join(patterns))
    lines = report_content.splitlines()
    clean_lines = [line for line in lines if not ignore_pattern.search(line)]
    return "\n".join(clean_lines)

# --- 輔助函式：取得適合的中文字型 ---
def get_chinese_font():
    """根據作業系統回傳適合的中文字型名稱"""
    system_name = platform.system()
    if system_name == "Windows":
        return "Microsoft JhengHei UI" # 微軟正黑體
    elif system_name == "Darwin": # macOS
        return "PingFang TC" # 蘋方體
    else: # Linux / 其他
        # Linux 常見中文字型，若系統沒安裝這些，還是會亂碼，需參考方案二
        return "WenQuanYi Micro Hei" 

# --- 介面控制區 (GUI) ---
def run_gui():
    window = tk.Tk()
    window.title("病歷報告去識別化工具 v1.0")
    window.geometry("600x700")

    # 取得當前系統適合的字型
    my_font = (get_chinese_font(), 10)
    my_font_bold = (get_chinese_font(), 10, "bold")
    btn_font = (get_chinese_font(), 12, "bold")

    def on_process_click():
        req_no = entry_no.get().strip()
        raw_content = text_input.get("1.0", tk.END)

        if not raw_content.strip():
            messagebox.showwarning("警告", "請輸入報告內容！")
            return

        result_content = core_deidentify_logic(raw_content)

        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, f"檢查單號: {req_no}\n")
        text_output.insert(tk.END, "-" * 30 + "\n")
        text_output.insert(tk.END, result_content)
        text_output.config(state=tk.DISABLED)

    # --- 版面配置 (套用新字型) ---
    
    lbl_no = tk.Label(window, text="檢查單號 (ExaRequestNo):", font=my_font_bold)
    lbl_no.pack(pady=(10, 5), anchor="w", padx=10)

    entry_no = tk.Entry(window, width=30, font=my_font)
    entry_no.pack(pady=5, anchor="w", padx=10)

    lbl_input = tk.Label(window, text="原始報告內容 (請貼上):", font=my_font_bold)
    lbl_input.pack(pady=(10, 5), anchor="w", padx=10)

    text_input = scrolledtext.ScrolledText(window, height=10, font=my_font)
    text_input.pack(padx=10, fill=tk.BOTH, expand=True)

    btn_run = tk.Button(window, text="執行去識別化轉換", command=on_process_click, 
                        bg="#0078D7", fg="white", font=btn_font, height=2)
    btn_run.pack(pady=10, fill=tk.X, padx=10)

    lbl_output = tk.Label(window, text="處理結果:", font=my_font_bold)
    lbl_output.pack(pady=(10, 5), anchor="w", padx=10)

    text_output = scrolledtext.ScrolledText(window, height=10, state=tk.DISABLED, bg="#f0f0f0", font=my_font)
    text_output.pack(padx=10, fill=tk.BOTH, expand=True, pady=(0, 10))

    window.mainloop()

if __name__ == "__main__":
    run_gui()