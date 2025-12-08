# import math

# print(f"2 + 2 = {2 + 2}")
# print(f"50 - 5*6 = {50 - 5*6}")
# print(f"(50 - 5*6) / 4 = {(50 - 5*6) / 4}")
# print(f"8 / 5 = {8 / 5}") # 除法總是回傳浮點數
# print(f"**********************")
# print(f"17 / 3  = {17 / 3}")# 傳統除法回傳浮點數
# print(f"17 // 3 = {17 // 3}")# 下取整除法捨棄小數部分
# print(f"17 % 3 = {17 % 3}")# % 運算子回傳除法的餘數
# print(f"5 * 3 + 2  = {5 * 3 + 2}")# 下取整商 * 除數 + 餘數
# print(f"**********************")
# print(f"5 ** 2  = {5 ** 2}")# 5 的平方
# print(f"2 ** 7   = {2 ** 7}")# 2 的七次方
# print(f"**********************")
# width = 20
# height = 5 * 9
# print(f"width * height = {width * height}")
# print(f"**********************")

# # print(n)

# print(f"round(2.9) = {round(2.9)}")
# print(f"abs(-2.9) = {abs(-2.9)}")
# print(f"math.ceil(2.2) = {math.ceil(2.2)}")
# print(f"**********************")
# x  =input("X: ")
# print(type(x))
# y = int(x) + 1
# print(f"x:{x}, y:{y}")
# print(f"**********************")
# print(f"bool(0):{bool(0)}")
# print(f"bool(1):{bool(1)}")
# print(f"bool(-1):{bool(-1)}")
# print(f"bool(5):{bool(5)}")
# print(f"bool(''):{bool('')}")
# print(f"bool('FALSE'):{bool('FALSE')}")
# print(f"**********************")
# fruit="Apple"
# print(f"fruit[1]:{fruit[1]}")
# print(f"fruit[1:-1]:{fruit[1:-1]}")#-1表示倒數第一個,不包含-1
# print(f"**********************")
# print(f"10 > 3:{10 > 3}")#True
# print(f"10 >= 3:{10 >= 3}")#True
# print(f"10 <= 20 :{10 <= 20}")#True
# print(f"10 == 20 :{10 == 20}")#True
# print(f"'bag' > 'apple' :{"bag">"apple"}")#True
# print(f"ord('b'):{ord('b')}")  # 輸出: 98
# print(f"ord('a'):{ord('a')}")  # 輸出: 97
# print(f"'bag' == 'BAG' :{"bag" =="BAG"}")#True
# print(f"ord('b'):{ord('b')}")  # 輸出: 98
# print(f"ord('B'):{ord('B')}")  # 輸出: 66
# temperature = 35
# if temperature > 30:
#     print("It's water")
#     print("Drink water")
# elif temperature > 20:
#     print("It's nice")
# else:
#     print("It's cold")

# print("Done")
# print(f"**********************")
# # age = 22
# age = 19
# # if age >= 18:
# #     message="Eligible"
# # else:
# #     message="Not eligible"

# message = "Eligible" if age >= 18 else "Not eligible"
# print(f"message:{message}")
# print("**********************")
# 高收入 = False
# 良好信用 = True
# 學生 = False
# if 高收入 and 良好信用:
#     print("核貸通過")
# else:
#     print("核貸不通過")

# if 高收入 or 良好信用:
#     print("核貸通過")
# else:
#     print("核貸不通過")

# if not 學生:
#     print("核貸通過")
# else:
#     print("核貸不通過")

# if (高收入 or 良好信用) and not 學生:
#     print("核貸通過")
# else:
#     print("核貸不通過")
# print("**********************")
# age = 22
# # if age >= 18 and age < 65:
# #     print("核貸通過")

# if 18 <= age < 65:
#     print("核貸通過")
# print("**********************")
# if 10 == "10":
#     print("a")
# elif "bag" > "apple" and "bag" > "cat":
#     print("b")
# else:
#     print("c")
# print(80 * "*")
# for number in range(3):
#     print(f"Hello World {number}")
#     print("Attempt", number + 1, (number + 1) * ".", number + 2, sep=" - ")

# print(80 * "*")
# for number in range(1,10,5):
#     print(f"Hello World {number}")
#     # print("Attempt", number + 1, (number + 1) * ".")

# successful = False
# print(80 * "*")
# for number in range(3):
#     print("Attempt")
#     if successful:
#         print("Successful")
#         break
# else:
#     print("Attempted 3 times and failed")
# print(80 * "*")
# for x in range(5):
#     for y in range(3):
#         print(f"(x:{x}, y:{y})")
# print(80 * "*")
# for x in range(5):
#     print(f"x:{x}")
# print(80 * "*")
# print(f"type(5):{type(5)}")
# print(f"type(range(5)):{type(range(5))}")
# print(80 * "*")
# for x in "Python":
#     print(f"x:{x}")

# print(80 * "*")
# for x in [1,2,3,4,5]:
#     print(f"x:{x}")

# print(80 * "*")
# shopping_cart = ["apple", "banana", "orange"]
# for item in shopping_cart:
#     print(f"item:{item}")
# print(80 * "*")
# number = 100
# while number > 0:
#     print(f"number:{number}")
#     number //= 2

# print(80 * "*")
# command = ""
# while command.lower() != "quit":
#     command = input(">")
#     print(f"command:{command}")
# print(80 * "*")
# while True:
#     command = input(">")
#     if command.lower() == "quit":
#         break
#     print(f"command:{command}")

# print(80 * "*")
# count = 0
# for number in range(1, 10):
#     if number % 2 == 0:
#         count+=1
#         print(f"number:{number}")

# print(f"Total even numbers: {count}")
# print(80 * "*")
# def greet():
#     print("Hello")
#     print("Welcome to the function demo")


# greet()

# print(80 * "*")
# def greet(first_name, last_name):
#      print(f"Hello {first_name} {last_name}")
#      print("Welcome to the function demo")


# greet("John", "Smith")
# print(80 * "*")
# def greet(name):
#      print(f"Hi {name}")
#      print("Welcome to the function demo")

# def get_greeting(name):
#     return f"Hi {name}!"

# message = get_greeting("John")
# file= open("content.txt", 'w')
# file.write(message)
# file.close()
# print(message)
# print(get_greeting("Mary"))
# print(80 * "*")
# def increment(number, by):
#     return number + by

# result = increment(2, 1)
# print(result)
# print(increment(2, 2))
# print(increment(number=3, by=4))

# print(80 * "*")
# def increment2(number, by=1):
#     return number + by

# result = increment2(2, 1)
# print(result)
# print(increment2(2))
# print(increment2(number=3, by=4))
# print(80 * "*")
# def multiply(*numbers):
#     # print(f"numbers:{numbers}")
#     for number in numbers:
#         print(f"number:{number}")

# # print(multiply(2, 3))
# multiply(2, 3, 4, 5)

print(80 * "*")
def multiply(*numbers):
    total = 1
    for number in numbers:
        total *= number
    return total


# print(multiply(2, 3))
print(multiply(2, 3, 4, 5))
