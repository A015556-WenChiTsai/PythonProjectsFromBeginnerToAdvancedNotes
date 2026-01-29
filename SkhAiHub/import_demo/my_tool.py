# 檔名：my_tool.py

def say_hello():
    print("你好！我是 my_tool 裡的函數。")

if __name__ == "__main__":
    # 當你直接按 Shift+Enter 執行這個檔案時，會跑這裡
    print(f"【主場模式】目前的身份是: {__name__}")
    say_hello()
else:
    # 當別的檔案寫 import my_tool 時，會跑這裡
    print(f"【客場模式】目前的身份是: {__name__}")