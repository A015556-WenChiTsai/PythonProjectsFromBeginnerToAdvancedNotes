class Encrypt:
    def __init__(self):
        self.send = ""  # 用來儲存原始輸入的字串
        self.res = []   # 用來儲存加密後的數字列表 (Result)

    # Sender encrypts the data
    def sender(self):
        self.send = input("Enter the data: ")  # 1. 獲取使用者輸入
        
        # 2. 加密核心邏輯：
        # ord(i) 將字元轉為整數代碼 (例如 'a' -> 97)
        # + 2 將代碼往後移兩位 (例如 97 -> 99)
        self.res = [ord(i) + 2 for i in self.send] 
        
        # 3. 顯示加密後的亂碼：
        # chr(i) 將整數轉回字元
        # "".join(...) 將字元列表合併成字串印出
        print("Encrypted data:", "".join(chr(i) for i in self.res))
        
class Decrypt(Encrypt):  # 繼承自 Encrypt 類別
    # Receiver decrypts the data
    def receiver(self):
        # 1. 解密核心邏輯：
        # 從 self.res 取出加密過的數字
        # i - 2 將數值減回去 (還原)
        # chr(...) 轉回原本的字元
        decrypted_data = "".join(chr(i - 2) for i in self.res)
        
        # 2. 印出解密後的原始資料
        print("Decrypted data:", decrypted_data)        
        
obj = Decrypt()   # 建立一個 Decrypt 物件 (同時也擁有 Encrypt 的功能)
obj.sender()      # 呼叫父類別的方法：輸入資料並加密
obj.receiver()    # 呼叫子類別的方法：解密資料        