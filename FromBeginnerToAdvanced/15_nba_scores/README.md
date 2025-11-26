# Python 網路爬蟲與資料處理實戰範例 (JSONPlaceholder)

這是一個示範如何撰寫**結構化**、**健壯**且**具備型別檢查**的 Python 網路請求腳本。
本專案模擬從 API 獲取使用者資料，並進行資料清洗（過濾）與排序，最後格式化輸出結果。

## 🎯 你將學到的核心觀念

透過這個範例，你將掌握以下 Python 企業級開發技巧：

1.  **Logging 機制**：使用 `logging` 取代 `print`，實現分級日誌與時間戳記。
2.  **HTTP Session 管理**：使用 `requests.Session` 與 Context Manager (`with`) 進行高效能連線。
3.  **錯誤處理**：優雅地處理網路異常 (`RequestException`) 與 HTTP 錯誤狀態。
4.  **資料處理技巧**：
    *   **List Comprehension**：快速過濾資料 (Filtering)。
    *   **Lambda Functions**：自定義排序邏輯 (Sorting)。
5.  **型別提示 (Type Hinting)**：使用 `typing` 模組提升程式碼可讀性與維護性。
6.  **格式化輸出**：使用 f-string 進行文字對齊，製作美觀的 CLI 報表。

## 🛠️ 環境需求

*   Python 3.6+
*   第三方套件：`requests`

### 安裝依賴

```bash
pip install requests