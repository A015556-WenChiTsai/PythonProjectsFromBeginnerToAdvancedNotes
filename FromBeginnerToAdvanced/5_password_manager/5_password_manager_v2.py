from cryptography.fernet import Fernet


# key+password+text
# 補充：相關方法
# rstrip(): 移除右側（末尾）的空白字元（包括空格、Tab \t、換行符 \n 等）。
# lstrip(): 移除左側（開頭）的空白字元。
# strip(): 移除兩側（開頭和末尾）的空白字元。
# pip install cryptography

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
"""key.key產生了一次性金鑰，用於加密和解密操作。
"""
write_key()

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


print(load_key())#讀出key

master_pwd = input("請輸入密碼: ")
key = load_key() + master_pwd.encode()
fer = Fernet(key)


def view():
    while True:
        with open("passwords.txt", "r") as f:
            for line in f.readlines():  #
                print("Line:", line.rstrip())  # 讀取每一行並去除換行符號
                # print("Line:", line)# 讀取每一行並去除換行符號
                data = line.rstrip()
                user, passw = data.split("|")
                print("帳戶名稱:", user, "| 密碼:", fer.decrypt(passw.encode())).decode()

                # data = line.rstrip()
                # user, pwd = data.split("|")
                # print("帳戶名稱:", user, "| 密碼:", pwd)
        break
    # print("Tim")
    pass


def add():
    name = input("帳戶名稱: ")
    pwd = input("密碼: ")
    # 讀取模式
    # with open('passwords.txt', 'r') as file:
    with open("passwords.txt", "a") as f:
        # f.write(name + "|" + str(fer.encrypt(pwd.encode()) + "\n"))
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
        # file.close()
    # file = open('passwords.txt', 'a')

    # print("密碼已儲存。")


while True:
    mode = input("你要查看密碼還是增加新密碼 (view/add)?: ").lower()
    if mode == "quit":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("無效的模式選擇。")
        continue
