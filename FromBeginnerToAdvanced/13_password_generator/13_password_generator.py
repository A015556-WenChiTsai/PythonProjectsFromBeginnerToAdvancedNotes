import secrets  # 用於產生加密隨機密碼
import string   # 用於字元集
import math     # 用於計算密碼熵
import logging  # 【新增】用於記錄程式運行細節

# 設定 Logging 的格式與等級
# level=logging.DEBUG 代表我們會記錄所有細節（包含變數變化）
# format 設定輸出的樣子：時間 - 等級 - 訊息
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)

def generate_password(length=12):
    """Generates a secure password of a given length."""
    logging.info(f"準備產生密碼，目標長度: {length}")
    
    logging.info(f"string.ascii_letters: {string.ascii_letters}")#abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    logging.info(f"string.digits: {string.digits}")#0123456789
    logging.info(f"string.punctuation: {string.punctuation}")#!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    characters = string.ascii_letters + string.digits + string.punctuation
    # logging.debug(f"使用的字元集總長度: {len(characters)}") # 想看細節可以打開這行
    
    password = ''.join(secrets.choice(characters) for _ in range(length))
    # === 傳統寫法 (新手易懂版) ===+
    # password_list = []                 # 1. 準備一個空籃子
    # for i in range(length):            # 2. 跑 12 次迴圈
    #     char = secrets.choice(characters)  # 3. 每次抓一個字
    #     password_list.append(char)     # 4. 丟進籃子裡

    # password = "".join(password_list)  # 5. 把籃子裡的東西黏起來
    
    
    logging.info(f"password: {password}")
    logging.info(f"password[:2]: {password[:2]}")#顯示前兩個字元
    logging.info(f"password[-2:]: {password[-2:]}")#顯示後兩個字元
    logging.debug(f"密碼產生完成 (隱藏部分內容): {password[:2]}***{password[-2:]}")
    
    
    
    return password

def calculate_entropy(password):
    """Calculates entropy (bits of security) for a given password."""
    logging.info("--- 開始計算密碼熵 ---")
    
    char_pool = 0
    logging.debug(f"初始字元池大小 (char_pool): {char_pool}")

    # 逐步檢查並記錄變數變化
    if any(c.islower() for c in password):
        char_pool += 26
        logging.debug(f"發現小寫字母 -> char_pool 增加為: {char_pool}")
    
    if any(c.isupper() for c in password):
        char_pool += 26
        logging.debug(f"發現大寫字母 -> char_pool 增加為: {char_pool}")
    
    if any(c.isdigit() for c in password):
        char_pool += 10
        logging.debug(f"發現數字 -> char_pool 增加為: {char_pool}")
    
    if any(c in string.punctuation for c in password):
        char_pool += len(string.punctuation)
        logging.debug(f"發現特殊符號 -> char_pool 增加為: {char_pool}")
    
    logging.debug(f"最終字元池大小 (R): {char_pool}")
    logging.debug(f"密碼長度 (L): {len(password)}")

    # 計算過程
    try:
        logging.info(f"char_pool ** len(password):{char_pool ** len(password)}")
        logging.info(f"math.log2(char_pool ** len(password):{math.log2(char_pool ** len(password))}")
        entropy = math.log2(char_pool ** len(password))
        logging.debug(f"計算公式: log2({char_pool}^{len(password)}) = {entropy:.4f}")
    except ValueError:
        logging.error("字元池為 0，無法計算熵值（可能是空密碼）")
        entropy = 0

    return entropy

if __name__ == "__main__":
    print("===== Secure Password Generator(安全密碼產生器) =====")
    logging.info("程式啟動")
    
    while True:
        try:
            user_input = input("Enter desired password length(輸入想要的密碼長度): ")
            length = int(user_input)
            logging.info(f"使用者輸入長度: {length}")
        except ValueError:
            logging.warning(f"使用者輸入無效: {user_input}")
            print("❌ 請輸入有效的數字！")
            continue
        
        password = generate_password(length)
        entropy = calculate_entropy(password)

        print(f"\n密碼: {password}")
        print(f"密碼熵: {entropy:.2f} 位元")
    
        if entropy < 50:
            logging.info("評級: 弱密碼")
            print("⚠️ 弱密碼！建議使用更多字元。")
        elif entropy < 80:
            logging.info("評級: 中等密碼")
            print("✅ 中等密碼。可以更強一些。")
        else:
            logging.info("評級: 強密碼")
            print("🔒 強密碼！非常安全。")
        
        user_choice = input("你對這個密碼滿意嗎？ (是/否): ").strip().lower()
        logging.info(f"使用者選擇: {user_choice}")

        if user_choice == '是':
            print("✅ 密碼已確定。")
            logging.info("程式正常結束")
            break
        else:
            print("🔄 生成新密碼中...\n")