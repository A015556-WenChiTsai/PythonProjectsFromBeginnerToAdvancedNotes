class Encrypt:
    def __init__(self):
        self.send = ""
        self.res = []

    # 修改這裡：讓 sender 接收參數 (text)，而不是用 input()
    def sender(self, text):
        self.send = text  # 直接使用傳入的文字
        self.res = [ord(i) + 2 for i in self.send]
        print("Encrypted data:", "".join(chr(i) for i in self.res))

class Decrypt(Encrypt):
    def receiver(self):
        decrypted_data = "".join(chr(i - 2) for i in self.res)
        print("Decrypted data:", decrypted_data)

# --- 使用方式 ---
obj = Decrypt()

# 在這裡直接填入你想測試的文字
target_text = "https://x.com/clcoding" 

print(f"Original data: {target_text}")
obj.sender(target_text)  # 把文字傳進去
obj.receiver()