import time

# ==========================================
# 情境：我們要在一個檔案清單中，搜尋是否有「病毒.exe」
# ==========================================
files_in_folder = ["report.doc", "image.jpg", "music.mp3", "backup.zip"]

# ==========================================
# 方法一：傳統寫法 (The Flag Pattern)
# 適用於：C, Java, C++ 轉過來的工程師
# ==========================================
def scan_traditional(target_file):
    print(f"\n--- [方法一] 傳統寫法啟動：搜尋 {target_file} ---")
    
    # 1. 【立旗】先假設沒找到 (False)
    is_found = False 

    for file in files_in_folder:
        print(f"正在掃描檔案: {file}...")
        time.sleep(0.3) # 模擬掃描時間
        
        if file == target_file:
            print(f"⚠️ 警告！發現目標檔案：{file} (觸發 Break)")
            # 2. 【舉旗】標記找到了
            is_found = True
            break # 既然找到了，後面就不用掃了
    
    # 3. 【檢查旗子】迴圈結束後，檢查變數狀態
    if is_found == False:
        print(f"✅ 安全回報：掃描完畢，未發現 {target_file}")

# ==========================================
# 方法二：Python 特有寫法 (For-Else)
# 適用於：追求程式碼簡潔的 Python 工程師
# ==========================================
def scan_pythonic(target_file):
    print(f"\n--- [方法二] Pythonic 寫法啟動：搜尋 {target_file} ---")
    
    for file in files_in_folder:
        print(f"正在掃描檔案: {file}...")
        time.sleep(0.3)
        
        if file == target_file:
            print(f"⚠️ 警告！發現目標檔案：{file} (觸發 Break)")
            break # 找到了，直接中斷！(注意：這會跳過 else 區塊)
    else:
        # 只有當迴圈「順利跑完」且「從未被 break 中斷」時，才會執行這裡
        # 不需要額外的 is_found 變數
        print(f"✅ 安全回報：掃描完畢，未發現 {target_file}")

# ==========================================
# 執行測試區
# ==========================================

print("=== 測試 A：尋找不存在的檔案 (應該顯示安全) ===")
# 傳統寫法
scan_traditional("virus.exe")
# Python 寫法
scan_pythonic("virus.exe")


print("\n\n" + "="*50 + "\n")


print("=== 測試 B：尋找存在的檔案 (應該顯示警告) ===")
# 傳統寫法
scan_traditional("image.jpg")
# Python 寫法
scan_pythonic("image.jpg")