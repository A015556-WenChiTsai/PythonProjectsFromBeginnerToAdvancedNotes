import sys
from dataclasses import dataclass, field
from typing import List

# ==========================================
# 場景 1: 傳統寫法 (Without Dataclass)
# ==========================================
class RegularProduct:
    """
    這是傳統的寫法。
    缺點：
    1. 必須手寫 __init__，重複 self.x = x
    2. 必須手寫 __repr__ 才能在 print 時看懂
    3. 必須手寫 __eq__ 才能比較兩個物件的內容
    """
    def __init__(self, name: str, price: float, tags: List[str] = None):
        self.name = name
        self.price = price
        self.tags = tags if tags is not None else []

    # 如果不寫這個，print 出來會是 <__main__.RegularProduct object at 0x...>
    def __repr__(self):
        return f"RegularProduct(name='{self.name}', price={self.price}, tags={self.tags})"

    # 如果不寫這個，p1 == p2 會是 False，因為它們記憶體位置不同
    def __eq__(self, other):
        if not isinstance(other, RegularProduct):
            return NotImplemented
        return (self.name, self.price, self.tags) == (other.name, other.price, other.tags)


# ==========================================
# 場景 2: Dataclass 寫法 (With Dataclass)
# ==========================================
@dataclass
class DataProduct:
    """
    這是 Pythonic 的寫法。
    優點：
    1. 自動生成 __init__, __repr__, __eq__
    2. 支援型別提示 (Type Hints)
    3. 支援預設值 (Default values)
    """
    name: str
    price: float
    # 對於可變物件(如 list)，使用 field(default_factory=...) 是更安全的做法
    tags: List[str] = field(default_factory=list) 

    @property
    def description(self) -> str:
        """仍然可以像普通類別一樣添加方法或屬性"""
        return f"{self.name} costs ${self.price}"


# ==========================================
# 執行與測試
# ==========================================
def main():
    print("--- 1. 程式碼簡潔度比較 ---")
    print("傳統類別需要寫約 15 行代碼來處理基礎功能。")
    print("Dataclass 只需要定義欄位，裝飾器會自動處理剩下的一切。\n")

    # 建立物件
    reg_p1 = RegularProduct("Laptop", 1000.0, ["tech"])
    reg_p2 = RegularProduct("Laptop", 1000.0, ["tech"])
    
    data_p1 = DataProduct("Laptop", 1000.0, tags=["tech"])
    data_p2 = DataProduct("Laptop", 1000.0, tags=["tech"])

    print("--- 2. 顯示效果 (__repr__) ---")
    print(f"傳統: {reg_p1}") 
    # 如果沒寫 __repr__，傳統類別會顯示類似 <__main__.RegularProduct object at 0x104...>
    print(f"Data: {data_p1}") 
    # Dataclass 自動生成漂亮的字串
    print()

    print("--- 3. 相等性比較 (__eq__) ---")
    print(f"傳統 (p1 == p2): {reg_p1 == reg_p2}") 
    # 如果沒寫 __eq__，這裡會是 False
    print(f"Data (p1 == p2): {data_p1 == data_p2}") 
    # Dataclass 自動比較內容值
    print()

    print("--- 4. 額外功能 ---")
    print(f"方法調用: {data_p1.description}")
    
    # Dataclass 也可以設定為不可變 (frozen=True)，類似 Tuple
    @dataclass(frozen=True)
    class FrozenItem:
        id: int
        name: str
    
    item = FrozenItem(1, "Ice")
    try:
        item.name = "Water" # 這行會報錯，因為它是唯讀的
    except Exception as e:
        print(f"不可變測試: 試圖修改 frozen dataclass 導致錯誤 -> {e}")

if __name__ == "__main__":
    main()