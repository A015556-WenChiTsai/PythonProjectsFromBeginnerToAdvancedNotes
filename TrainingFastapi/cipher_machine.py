from dataclasses import dataclass

@dataclass
class CipherMachine:
    """
    一個簡單的加密/解密機器
    """
    shift: int = 2  # 預設位移量為 2，也可以在建立物件時修改
    
    def encrypt(self, text: str) -> str:
        """加密：將文字轉為 ASCII 後加上位移量"""
        # Pythonic 寫法：生成器表達式直接在 join 裡面運作
        return "".join(chr(ord(char) + self.shift) for char in text)

    def decrypt(self, encrypted_text: str) -> str:
        """解密：將加密文字轉為 ASCII 後減去位移量"""
        return "".join(chr(ord(char) - self.shift) for char in encrypted_text)

# --- 執行區 (Shift + Enter 直接看結果) ---

# 1. 準備資料
original_data = "https://x.com/clcoding"

# 2. 初始化物件 (使用 DataClass 自動生成的 init)
# 你也可以改成 CipherMachine(shift=3) 來改變加密規則
machine = CipherMachine() 

# 3. 執行加密
encrypted_data = machine.encrypt(original_data)

# 4. 執行解密
decrypted_data = machine.decrypt(encrypted_data)

# 5. 漂亮的輸出結果 (使用 f-string)
print(f"{'='*30}")
print(f"原始資料 : {original_data}")
print(f"加密結果 : {encrypted_data}")
print(f"解密驗證 : {decrypted_data}")
print(f"{'='*30}")

# 驗證是否還原成功
assert original_data == decrypted_data
print("✅ 驗證成功：解密後的資料與原始資料完全一致！")