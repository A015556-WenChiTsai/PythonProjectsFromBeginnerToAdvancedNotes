# 🔐 Secure Password Generator (安全密碼產生器)

這是一個基於 Python 的安全密碼生成工具。它不僅能產生高強度的隨機密碼，還能即時計算密碼的「熵值 (Entropy)」，讓使用者直觀地了解密碼的安全性強度。

## 🚀 專案特色 (Features)

- **加密級隨機性**：使用 Python 內建的 `secrets` 模組，確保密碼無法被預測（優於 `random` 模組）。
- **熵值計算 (Entropy Calculation)**：根據字元集大小與密碼長度，科學地計算密碼強度（位元數）。
- **強度評級**：自動判斷密碼為「弱」、「中等」或「強」。
- **互動式介面**：使用者可以自訂長度，並決定是否接受生成的密碼。

## 📚 你將在這個專案中學到的 Python 觀念

1.  **模組應用**：
    - `secrets`: 用於生成加密安全的隨機數。
    - `string`: 快速獲取字母、數字和符號集合。
    - `math`: 使用對數函數計算資訊熵。
2.  **字串處理**：使用 `join` 方法與 List Comprehension 高效生成字串。
3.  **邏輯判斷**：使用 `any()` 函數與生成器表達式來檢查字元類型。
4.  **流程控制**：`while` 迴圈、`if/elif/else` 條件判斷與使用者輸入處理。
5.  **程式結構**：使用 `if __name__ == "__main__":` 建立標準程式入口。

## 🛠️ 安裝與執行 (Installation & Usage)

### 前置需求
- Python 3.6 或更高版本

### 執行步驟

1. 下載或建立 `password_generator.py` 檔案。
2. 在終端機 (Terminal) 執行以下指令：

```bash
python password_generator.py