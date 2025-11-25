# password_manager.py

import random
import secrets
import string
import os

# 儲存密碼的檔案名稱
PASSWORD_FILE = "passwords.txt"
# 預設的主密碼 (請在實際使用中替換為更複雜的密碼)
MASTER_PASSWORD = "mysecretmasterkey" 

def check_master_password():
    """
    驗證使用者輸入的主密碼。
    """
    attempt = input("請輸入主密碼以繼續: ")
    if attempt == MASTER_PASSWORD:
        return True
    else:
        print("主密碼錯誤！")
        return False

def generate_password(length=16):
    """
    使用 secrets 模組生成一個安全的隨機密碼。
    """
    # 包含字母大小寫、數字和標點符號
    alphabet = string.ascii_letters + string.digits + string.punctuation
    
    # 確保密碼至少包含一個大寫、一個小寫、一個數字和一個符號
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # 填充剩餘長度
    for _ in range(length - 4):
        password.append(secrets.choice(alphabet))
        
    # 隨機打亂順序
    random.shuffle(password)
    
    return "".join(password)

def add_password():
    """
    新增一組帳號/密碼到檔案中。
    """
    service = input("請輸入服務名稱 (例如: Google, Facebook): ")
    username = input("請輸入帳號/使用者名稱: ")
    
    # 詢問是否要生成密碼
    gen_choice = input("是否要自動生成一個強密碼？ (y/n): ").lower()
    
    if gen_choice == 'y':
        password = generate_password()
        print(f"已生成密碼: {password}")
    else:
        password = input("請輸入您要儲存的密碼: ")
        
    # 格式化儲存的字串： 服務 | 帳號 | 密碼
    entry = f"{service} | {username} | {password}\n"
    
    try:
        # 使用 'a' 模式 (append) 將新密碼追加到檔案末尾
        with open(PASSWORD_FILE, 'a') as f:
            f.write(entry)
        print(f"\n密碼已成功儲存到 {service}。")
    except Exception as e:
        print(f"儲存時發生錯誤: {e}")

def view_passwords():
    """
    讀取並顯示所有儲存的密碼。
    """
    if not os.path.exists(PASSWORD_FILE):
        print("目前沒有儲存任何密碼。")
        return

    print("\n--- 儲存的密碼 ---")
    try:
        with open(PASSWORD_FILE, 'r') as f:
            for line in f:
                # 移除換行符並顯示
                print(line.strip())
        print("------------------")
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")

def main():
    """
    主程式邏輯和選單。
    """
    if not check_master_password():
        return

    while True:
        print("\n--- 密碼管理器選單 ---")
        print("1. 新增密碼")
        print("2. 查看所有密碼")
        print("3. 生成一個強密碼")
        print("4. 退出")
        
        choice = input("請選擇操作 (1-4): ")
        
        if choice == '1':
            add_password()
        elif choice == '2':
            view_passwords()
        elif choice == '3':
            length = input("請輸入密碼長度 (預設 16): ")
            try:
                length = int(length) if length else 16
                print(f"生成的密碼: {generate_password(length)}")
            except ValueError:
                print("長度輸入無效。")
        elif choice == '4':
            print("感謝使用，再見！")
            break
        else:
            print("無效的選擇，請重新輸入。")

if __name__ == "__main__":
    # 確保 random 模組在生成密碼時能正常工作
    random.seed() 
    main()