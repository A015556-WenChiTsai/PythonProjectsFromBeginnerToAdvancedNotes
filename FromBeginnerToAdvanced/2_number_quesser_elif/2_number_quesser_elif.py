import random

# 範圍是從 -1 到 10 (包含 -1，不包含 11)
r1 = random.randrange(-1, 11)
# 範圍是從 0 到 10 (包含 0，不包含 11)
r2 = random.randrange(11)
# print(f"r1: {r1}")
# print(f"r2: {r2}")

top_of_range = input("請輸入你想要的最大數字: ")
# isdigit 方法來檢查輸入是否為數字
if top_of_range.isdigit():
    top_of_range = int(top_of_range)
    if top_of_range <= 0:
        print("請輸入大於0的數字。")
        quit()
else:
    print("請輸入數字。")
    quit()

rendowm_number = random.randrange(0, top_of_range)
guess = 0
print(rendowm_number)

while True:
    guess += 1
    user_guess = input("請猜一個數字: ")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("請猜一個數字: ")
        continue

    if user_guess == rendowm_number:
        print("你猜對了！")
        break
    elif user_guess > rendowm_number:
        print("你猜的數字太大了！")
    else:
        print("你猜的數字太小了！")
    # print("你猜錯了，請再試一次！")


print("你總共猜了 ", guess, "guess")
# print("你總共猜了 " + str(user_guess) + " 次數字才猜對。")
# print("你猜的數字是 " + str(user_guess))
