import random
import logging
from collections import Counter
from typing import List, Tuple

# ==========================================
# 1. Logging 設定
# ==========================================
# 設定日誌格式與輸出檔案
logging.basicConfig(
    filename='mastermind.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8' # 確保中文寫入不亂碼
)

# 常數定義 (使用 Tuple 避免被意外修改，且更省記憶體)
COLORS: Tuple[str, ...] = ("R", "G", "B", "Y", "O", "P")
TRIES: int = 10
CODE_LENGTH: int = 4

def generate_code() -> List[str]:
    """隨機生成一組密碼"""
    code = [random.choice(COLORS) for _ in range(CODE_LENGTH)]
    # code= list(('R', 'G', 'B', 'Y')) # for testing
    # 在開發或除錯時，記錄生成的密碼很有幫助（但在正式上線通常會隱藏）
    logging.info(f"新遊戲開始，生成的密碼為: {code}")
    return code

def get_valid_guess() -> List[str]:
    """
    獲取並驗證使用者的輸入。
    持續詢問直到獲得有效輸入為止。
    """
    while True:
        user_input = input(
            f"輸入你的猜測 ({CODE_LENGTH} 個字母，顏色範圍 {', '.join(COLORS)}): "
        ).upper().strip() # strip() 去除前後空白

        # 驗證長度
        if len(user_input) != CODE_LENGTH:
            msg = f"輸入長度錯誤: {len(user_input)} (需要 {CODE_LENGTH})"
            print(f"無效的輸入。{msg}")
            logging.warning(f"使用者輸入無效: {user_input} - 原因: {msg}")
            continue

        # 驗證顏色是否合法
        # 使用 set 的 issubset 來判斷是否所有字元都在 COLORS 裡，這很 Pythonic
        if not set(user_input).issubset(set(COLORS)):
            msg = "包含無效的顏色代碼"
            print(f"無效的輸入。{msg}，必須是 {', '.join(COLORS)} 之一。")
            logging.warning(f"使用者輸入無效: {user_input} - 原因: {msg}")
            continue

        return list(user_input)

def evaluate_guess(code: List[str], guess: List[str]) -> Tuple[int, int]:
    """
    評估猜測結果。
    回傳: (位置正確數, 顏色正確但位置錯誤數)
    """
    # 1. 計算位置完全正確的數量 (A)
    logging.info(f"code: {code}")#['R', 'G', 'B', 'Y']
    logging.info(f"guess: {guess}")#['R', 'O', 'B', 'P']
    logging.info(f"list(zip(code, guess)): {list(zip(code, guess))}")#[('R', 'R'), ('G', 'O'), ('B', 'B'), ('Y', 'P')]
    logging.info(f"[(c, g) for c, g in zip(code, guess)]): {[(c, g) for c, g in zip(code, guess)]}")#[('R', 'R'), ('G', 'O'), ('B', 'B'), ('Y', 'P')]
    correct_position = sum(c == g for c, g in zip(code, guess))
    # for c, g in ... 與 c == g：拆解與比對
    # 這是一個 生成器表達式 (Generator Expression)。它會遍歷上面那個「拉鍊」後的結果。
    # 第一組 ('R', 'R')：c是R, g是R。c == g 嗎？ True
    # 第二組 ('G', 'O')：c是G, g是O。c == g 嗎？ False
    # 第三組 ('B', 'B')：c是B, g是B。c == g 嗎？ True
    # 第四組 ('Y', 'P')：c是Y, g是P。c == g 嗎？ False
    logging.info(f"correct_position(計算位置完全正確的數量): {correct_position}")

    # 2. 計算顏色正確的總數 (包含位置正確和錯誤的)
    # 使用 Counter 可以輕鬆計算每個元素出現的次數
    # Counter(code) & Counter(guess) 會取出兩者間的「交集」（取最小計數）
    # 例如: Code有兩個R，Guess有一個R，交集就是一個R
    code_counts = Counter(code)
    logging.info(f"code_counts: {code_counts}")#Counter({'R': 1, 'G': 1, 'B': 1, 'Y': 1})
    guess_counts = Counter(guess)
    logging.info(f"guess_counts: {guess_counts}")#Counter({'R': 1, 'O': 1, 'B': 1, 'P': 1})
    logging.info(f"(code_counts & guess_counts): {(code_counts & guess_counts)}")#Counter({'R': 1, 'B': 1})
    total_color_match = sum((code_counts & guess_counts).values())
    logging.info(f"total_color_match(計算顏色正確的總數): {total_color_match}")

    # 3. 顏色正確但位置錯誤 (B) = 總顏色匹配數 - 位置完全正確數
    correct_color = total_color_match - correct_position
    logging.info(f"correct_color(顏色正確但位置錯誤): {correct_color}")
    return correct_position, correct_color

def main():
    print("歡迎來到大師班！(Mastermind)")
    
    try:
        code = generate_code()
        
        for attempt in range(1, TRIES + 1):
            print(f"\n--- 嘗試次數 {attempt} / {TRIES} ---")
            
            guess = get_valid_guess()
            logging.info(f"嘗試 #{attempt}: 使用者猜測 {guess}")

            correct_position, correct_color = evaluate_guess(code, guess)
            
            if correct_position == CODE_LENGTH:
                msg = f"恭喜！你猜對了密碼：{''.join(code)}"
                print(msg)
                logging.info(f"遊戲勝利 - {msg}")
                break
            else:
                print(f"位置正確: {correct_position}")
                print(f"顏色正確(位置錯): {correct_color}")
        else:
            # Python 的 for-else 語法：當迴圈沒有被 break 中斷時執行
            msg = f"很遺憾，你已經用完所有嘗試次數。密碼是：{''.join(code)}"
            print(msg)
            logging.info(f"遊戲失敗 - {msg}")

    except Exception as e:
        # ==========================================
        # 2. 捕捉未預期的 BUG 並寫入檔案
        # ==========================================
        error_msg = "遊戲發生未預期的錯誤"
        print(f"系統發生錯誤，請聯繫管理員。錯誤代碼已記錄。")
        # logging.exception 會自動把 Traceback (錯誤堆疊) 寫入檔案
        logging.exception(error_msg)

if __name__ == "__main__":
    main()