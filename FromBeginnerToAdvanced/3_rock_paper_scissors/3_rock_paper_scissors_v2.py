import random

user_wins = 0
computer_wins = 0

options = ["剪刀", "石頭", "布"]
# options2 = ['剪刀', '石頭', '布']
while True:
    user_input = input("請輸入您的選擇 (剪刀/石頭/布) 或輸入 'q' 退出: ")
    if user_input == 'q':
        break
    if user_input not in options:
        print("無效的選擇，請再試一次。")
        continue

    random_number = random.randint(0, 2)
     # 0 = 剪刀, 1 = 石頭, 2 = 布
    computer_pick = options[random_number]
     # computer_pick = options2[random_number]
     # print(f"電腦選擇了: {computer_pick}")    

    if user_input == "剪刀" and computer_pick == "布" or \
       user_input == "石頭" and computer_pick == "剪刀" or \
       user_input == "布" and computer_pick == "石頭":
        print("你贏了！")
        user_wins += 1
    elif user_input == computer_pick:
        print("平手！")
    else:
        print("你輸了！")
        computer_wins += 1  
    
print("遊戲結束！")
print(f"你贏了 {user_wins} 次，電腦贏了 {computer_wins} 次。")