import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. 設定 Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class CurrencyConverter:
    # 從你提供的網址中提取出的 Base URL 和 Key
    BASE_URL = "https://v6.exchangerate-api.com/v6"
    API_KEY = "51133b77835cd39065d85872" # 這是你網址裡的 Key

    def __init__(self):
        self.session = requests.Session()
        # 設定重試機制，避免網路閃斷
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # 這裡我們用一個變數來存 API 回傳的整包匯率表 (Cache)
        self.rates_cache = {} 
        logger.info("CurrencyConverter initialized.")

    def fetch_latest_rates(self):
        """
        從 API 獲取最新的 USD 基準匯率表。
        這會更新 self.rates_cache
        """
        endpoint = f"{self.BASE_URL}/{self.API_KEY}/latest/USD"
        
        logger.info(f"Fetching latest rates from API...")
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('result') == 'success':
                self.rates_cache = data.get('conversion_rates', {})
                logger.info(f"Successfully loaded {len(self.rates_cache)} currency rates.")
                return True
            else:
                logger.error("API returned error status.")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            return False

    def get_currencies(self):
        """
        回傳所有支援的貨幣代碼列表
        """
        # 如果快取是空的，先抓一次資料
        if not self.rates_cache:
            success = self.fetch_latest_rates()
            if not success:
                return []
        
        # 回傳所有貨幣代碼 (排序過)
        return sorted(self.rates_cache.keys())

    def convert(self, amount, base_currency, target_currency):
        """
        利用 USD 基準匯率進行換算 (Cross Rate Calculation)
        """
        # 確保有資料
        if not self.rates_cache:
            self.fetch_latest_rates()

        # 檢查貨幣是否存在
        if base_currency not in self.rates_cache or target_currency not in self.rates_cache:
            logger.warning(f"Currency not found: {base_currency} or {target_currency}")
            return None

        # 取得相對於 USD 的匯率
        # 例如: USD -> TWD = 31.41
        # 例如: USD -> JPY = 156.89
        base_rate_to_usd = self.rates_cache[base_currency]
        target_rate_to_usd = self.rates_cache[target_currency]

        # 計算公式: (金額 / 來源對美金匯率) * 目標對美金匯率
        # 邏輯: 先把來源貨幣轉成美金，再把美金轉成目標貨幣
        converted_amount = (amount / base_rate_to_usd) * target_rate_to_usd
        
        return converted_amount

    def close(self):
        self.session.close()

# --- 主程式邏輯 ---

def print_currencies(currencies):
    if not currencies:
        print("No currencies available.")
        return
    
    print("-" * 30)
    # 因為這個 API 只有代碼沒有全名，我們就每行印 5 個代碼，比較整齊
    for i in range(0, len(currencies), 5):
        print(" ".join(f"{code:<5}" for code in currencies[i:i+5]))
    print("-" * 30)

def main():
    converter = CurrencyConverter()
    
    try:
        # 程式啟動時先抓一次資料
        if not converter.fetch_latest_rates():
            print("Failed to initialize data. Please check your network or API Key.")
            return

        print("=== Currency Converter (Cached Version) ===")
        print("Data Source: ExchangeRate-API")
        
        while True:
            command = input("\nCommand (list, convert, q): ").strip().lower()

            if command == "q":
                print("Goodbye!")
                break
            
            elif command == "list":
                currencies = converter.get_currencies()
                print_currencies(currencies)
            
            elif command == "convert":
                c1 = input("Base Currency (e.g. TWD): ").upper()
                amount_str = input(f"Amount in {c1}: ")
                c2 = input("Target Currency (e.g. JPY): ").upper()
                
                try:
                    amount = float(amount_str)
                    result = converter.convert(amount, c1, c2)
                    
                    if result is not None:
                        # 計算單價匯率
                        rate = result / amount
                        print(f"\nResult: {amount:,.2f} {c1} = {result:,.2f} {c2}")
                        print(f"Exchange Rate: 1 {c1} = {rate:,.4f} {c2}")
                    else:
                        print("Invalid currency codes.")
                        
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            
            else:
                print("Unknown command.")

    finally:
        converter.close()

if __name__ == "__main__":
    main()