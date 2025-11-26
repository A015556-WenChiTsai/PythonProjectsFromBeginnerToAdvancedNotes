import time
import logging

# ==========================================
# 設定 Logging
# 檔名：benchmark_history.log
# filemode='a' (Append)：追加模式，不會清空舊資料，適合長期記錄效能
# ==========================================
logging.basicConfig(
    filename='benchmark_history.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a' 
)

def benchmark():
    # 1. 準備資料
    data_size = 100_000
    iterations = 1000
    target = -1  # 找一個不存在的數字 (最壞情況)

    # 在螢幕上提示一下，不然你會以為程式沒在跑
    print(f"🚀 正在執行效能測試 (規模: {data_size})... 請稍候")
    
    # 寫入 Log 標頭，區隔每一次執行
    logging.info("========================================")
    logging.info(f"🚀 開始新一輪測試")
    logging.info(f"📊 資料規模: {data_size} 筆 | 測試次數: {iterations} 次")

    # 準備 List 和 Set
    test_list = list(range(data_size))
    test_set = set(range(data_size))
    logging.info(f"test_list: {test_list} ")
    logging.info(f"test_set: {test_set} ")
    # ==========================================
    # 測試 List (O(n))
    # ==========================================
    start_time = time.time()
    for _ in range(iterations):
        if target in test_list:
            pass
    end_time = time.time()
    list_duration = end_time - start_time
    
    logging.info(f"🐢 List (列表) 耗時: {list_duration:.5f} 秒")

    # ==========================================
    # 測試 Set (O(1))
    # ==========================================
    start_time = time.time()
    for _ in range(iterations):
        if target in test_set:
            pass
    end_time = time.time()
    set_duration = end_time - start_time
    
    logging.info(f"⚡️ Set  (集合) 耗時: {set_duration:.5f} 秒")

    # ==========================================
    # 計算差異並記錄
    # ==========================================
    if set_duration > 0:
        ratio = list_duration / set_duration
        logging.info(f"🏆 結論: Set 比 List 快了 {ratio:.1f} 倍")
    else:
        logging.info("🏆 結論: Set 太快了，無法計算倍數")

    print("✅ 測試完成！請查看 benchmark_history.log")

if __name__ == "__main__":
    benchmark()