# rock_paper_scissors.py

import random

user_wins = 0
computer_wins = 0
def get_user_choice():
    """
    獲取使用者輸入的選擇，並進行驗證。
    """
    while True:
        # 提示使用者輸入，並將輸入轉換為小寫，方便比較(原來可以這樣用!!)
        user_input = input("請輸入您的選擇 (剪刀/石頭/布) 或輸入 'q' 退出: ").lower()
        
        if user_input == 'q':
            return 'q'
        
        if user_input in ['剪刀', '石頭', '布']:
            return user_input
        else:
            print("輸入無效，請重新輸入 (剪刀/石頭/布)。")

def get_computer_choice():
    """
    電腦隨機選擇剪刀、石頭或布。
    """
    choices = ['剪刀', '石頭', '布']
    print(choices[0])
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    """
    根據遊戲規則判斷勝負。
    """
    print(f"\n您的選擇: {user_choice}")
    print(f"電腦的選擇: {computer_choice}")
    
    if user_choice == computer_choice:
        return "平手"
    
    # 判斷使用者獲勝的條件
    if (user_choice == '石頭' and computer_choice == '剪刀') or \
       (user_choice == '剪刀' and computer_choice == '布') or \
       (user_choice == '布' and computer_choice == '石頭'):
        return "恭喜，您贏了！"
    else:
        return "很遺憾，電腦贏了！"

def play_game():
    """
    遊戲主循環。
    """
    print("--- 歡迎來到剪刀石頭布遊戲！ ---")
    
    while True:
        user_choice = get_user_choice()
        
        if user_choice == 'q':
            print("遊戲結束，感謝您的遊玩！")
            break
            
        computer_choice = get_computer_choice()
        
        result = determine_winner(user_choice, computer_choice)
        print(f"結果: {result}\n")

# 確保只有直接運行此檔案時才執行 play_game() 函式
if __name__ == "__main__":
    # 確保 random 模組在程式開始時被初始化
    random.seed() 
    play_game()