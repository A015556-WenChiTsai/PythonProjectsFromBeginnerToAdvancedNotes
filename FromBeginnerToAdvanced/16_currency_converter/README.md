# Python Currency Converter (匯率轉換器)

這是一個基於 Python 的匯率轉換工具，使用 `requests` 模組串接 ExchangeRate-API，並具備快取與自動重試機制。

## 專案特色 (Key Features)

這個專案展示了從「初學者」進階到「工程師」所需的關鍵技術：

1.  **REST API 串接**：從遠端伺服器獲取 JSON 格式的匯率資料。
2.  **穩健的網路請求**：
    *   使用 `requests.Session` 提升效能。
    *   實作 `Retry` 機制，自動處理網路瞬斷或伺服器錯誤 (5xx)。
3.  **快取機制 (Caching)**：將匯率資料暫存於記憶體，避免重複呼叫 API，節省額度並提升速度。
4.  **日誌系統 (Logging)**：使用標準 `logging` 模組取代 `print`，記錄程式運作狀態與錯誤。
5.  **物件導向 (OOP)**：將邏輯封裝於 `CurrencyConverter` 類別中，程式結構清晰。

## 環境需求 (Prerequisites)

請確保已安裝 Python 3.x，並安裝以下套件：

```bash
pip install requests