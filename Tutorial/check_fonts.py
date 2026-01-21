import tkinter as tk
from tkinter import font

root = tk.Tk()
all_fonts = list(font.families())
all_fonts.sort()

print("--- 系統可用字型列表 ---")
# 搜尋常見的中文字型關鍵字
chinese_fonts = [f for f in all_fonts if "wqy" in f.lower() or "micro" in f.lower() or "zen" in f.lower() or "noto" in f.lower() or "cjk" in f.lower()]

if chinese_fonts:
    print("找到中文字型：")
    for f in chinese_fonts:
        print(f"  -> {f}")
else:
    print("警告：沒有找到常見的中文字型！")
    print("前 20 個可用字型:", all_fonts[:20])

root.destroy()