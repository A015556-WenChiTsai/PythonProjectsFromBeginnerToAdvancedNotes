# Python Slot Machine (老虎機) 學習專案

這是一個基於 Python 的命令行老虎機遊戲。作為初學者，透過這個專案你可以掌握 Python 程式設計的核心邏輯與資料結構操作。

## 🎯 你將學到的核心概念 (Key Learning Points)

### 1. 基礎資料結構 (Data Structures)
*   **字典 (Dictionaries):** 
    *   程式中使用了 `symbol_count` 和 `symbol_value` 來儲存符號的數量與賠率。
    *   **學習點:** 如何使用 Key-Value 對來管理配置數據。
*   **列表 (Lists) 與 巢狀列表 (Nested Lists):**
    *   老虎機的滾輪（Columns）是使用列表來實作的，整個遊戲畫面是一個「列表的列表」（二維陣列）。
    *   **學習點:** 如何操作二維數據，例如 `columns[0][line]`。

### 2. 流程控制與迴圈 (Control Flow & Loops)
*   **While True 迴圈:** 
    *   在 `deposit()` 和 `get_bet()` 中，使用了無窮迴圈來強制使用者輸入正確的數值，直到條件滿足才 `break`。
    *   **學習點:** 這是處理「使用者輸入驗證」的標準寫法。
*   **For 迴圈與 Enumerate:**
    *   在 `print_slot_machine()` 中使用了 `enumerate` 來同時獲取索引(index)和值(value)。
    *   **學習點:** 優雅地遍歷列表。
*   **For...Else 用法:**
    *   在 `check_winnings` 函式中使用了 Python 特有的 `for...else` 語法。
    *   **學習點:** 當迴圈完整執行完且沒有被 `break` 中斷時，才會執行 `else` 區塊（用於判斷整行符號是否一致）。

### 3. 模組化程式設計 (Modular Programming)
*   **函式封裝 (Functions):**
    *   程式被拆分為多個功能單一的函式：`deposit` (存款), `spin` (旋轉邏輯), `check_winnings` (檢查輸贏)。
    *   **學習點:** 學習「單一職責原則」(Single Responsibility)，讓程式碼易於閱讀與除錯。

### 4. 隨機性與邏輯 (Randomness & Logic)
*   **Random 模組:**
    *   使用 `random.choice()` 從列表中隨機選取符號。
    *   **學習點:** 模擬機率事件。
*   **矩陣轉置邏輯 (Matrix Transposition):**
    *   **關鍵難點:** 程式產生的數據是 `columns` (直列)，但檢查輸贏和列印時需要按 `lines` (橫列) 處理。
    *   **學習點:** 學習如何在雙層迴圈中交換 `row` 和 `col` 的思維。

### 5. 字串處理與輸出 (String Formatting)
*   **f-string:** 大量使用 `f"..."` 來嵌入變數。
*   **Unpacking Operator (*):** 在 `print(*winning_lines)` 中使用了 `*` 運算符將列表解包成獨立參數列印。

---

## 🛠️ 程式碼結構分析

### 全域常數 (Global Constants)
```python
MAX_LINES = 3
MAX_BET = 100