# import logging
# import os

# # 設定 Log 格式與輸出檔案
# # encoding='utf-8' 確保中文不會變亂碼
# logging.basicConfig(
#     filename='list_learning.log',
#     level=logging.INFO,
#     format='%(asctime)s - [EXP] %(funcName)s - %(message)s',
#     encoding='utf-8',
#     filemode='w' # 每次執行都重寫，方便觀察
# )

# logger = logging.getLogger()

# print("程式執行中... 請查看目錄下的 list_learning.log 檔案")

# def demo_slicing_and_indexing():
#     """
#     情境：我們從資料庫撈出了一組 User ID，需要做分頁顯示，
#     並且快速查看最新註冊的用戶。
#     """
#     user_ids = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
#     logger.info(f"原始 User ID 列表: {user_ids}")

#     # 1. 獲取最新一筆資料 (Last item)
#     # Bad: last_user = user_ids[len(user_ids) - 1]
#     # Pythonic: 使用負數索引
#     last_user = user_ids[-1]
#     logger.info(f"最新註冊的 User ([-1]): {last_user}")

#     # 2. 獲取最後三筆資料 (Last N items) - 常見於 'Recent Activity' 功能
#     recent_users = user_ids[-3:]
#     logger.info(f"最近三位 User ([-3:]): {recent_users}")

#     # 3. 分頁 (Pagination) - 模擬每頁顯示 3 筆，取第 2 頁
#     page_size = 3
#     page_number = 2 # 假設是第 2 頁 (索引從 0 開始算，所以是 index 3 到 6)
#     start_idx = (page_number - 1) * page_size
#     end_idx = start_idx + page_size
    
#     # Pythonic: 切片操作 [start:end] (不包含 end)
#     page_data = user_ids[start_idx:end_idx]
#     logger.info(f"第 {page_number} 頁數據 (每頁{page_size}筆): {page_data}")

#     # 4. 淺拷貝 (Shallow Copy)
#     # 當你需要修改列表但不想影響原始資料時
#     backup_ids = user_ids[:] 
#     logger.info(f"備份列表 ([:]): {backup_ids}")
    
#     def demo_concatenation():
#     """
#     情境：合併兩個不同部門的員工名單。
#     """
#     dev_team = ['Alice', 'Bob']
#     ops_team = ['Charlie', 'Dave']
    
#     logger.info(f"開發組: {dev_team}, 維運組: {ops_team}")

#     # 1. 使用 + 號 (會產生一個全新的 List 物件)
#     # 適用於：你需要保留原始的兩個列表，產生第三個列表
#     all_staff_new = dev_team + ops_team
#     logger.info(f"合併後的新名單 (+): {all_staff_new}")

#     # 2. 使用 extend (原地修改)
#     # 適用於：你不再需要分開的 dev_team，想直接把人加進去，節省記憶體
#     # 這在處理大數據量時非常重要
#     dev_team.extend(ops_team)
#     logger.info(f"擴充後的開發組 (extend): {dev_team}")
    
#     def demo_mutability_and_replacement():
#     """
#     情境：有一組感測器數據，發現中間有一段時間數據異常(是 None 或 錯誤值)，
#     需要批量替換成預設值或修正值。
#     """
#     sensor_data = [22.5, 23.0, 999.9, 999.9, 999.9, 24.1, 24.5]
#     logger.info(f"原始感測器數據 (含異常): {sensor_data}")

#     # 1. 批量替換 (Slice Assignment)
#     # 我們知道 index 2 到 5 (不含) 是異常的，替換成平均值 23.5
#     # Pythonic: 直接對切片範圍賦值
#     sensor_data[2:5] = [23.5, 23.5, 23.5]
#     logger.info(f"修正後的數據 (Slice Assignment): {sensor_data}")

#     # 2. 刪除片段
#     # 假設最後兩筆數據無效，想直接移除
#     sensor_data[-2:] = []
#     logger.info(f"移除末尾兩筆後: {sensor_data}")

#     # 3. 清空列表
#     # 情境：處理完畢，清空 Buffer
#     sensor_data[:] = []
#     logger.info(f"清空後的列表: {sensor_data}")
    
#     def demo_nested_lists():
#     """
#     情境：一個 3x3 的矩陣 (Matrix)，代表井字遊戲 (Tic-Tac-Toe) 的狀態。
#     """
#     board = [
#         ['O', 'X', 'O'],
#         [' ', 'X', ' '],
#         [' ', ' ', 'X']
#     ]
#     logger.info(f"當前棋盤狀態: {board}")

#     # 1. 存取特定元素
#     # 獲取中間那個格子 (Row 1, Col 1)
#     center_piece = board[1][1]
#     logger.info(f"中心點棋子: {center_piece}")

#     # 2. 修改特定元素
#     # 玩家在 Row 2, Col 0 下了一步 'O'
#     board[2][0] = 'O'
#     logger.info(f"玩家下棋後 (board[2][0] = 'O'): {board}")
    
#     # 3. 扁平化 (Flatten) - 進階技巧 (雖然文檔沒深講，但這很常用)
#     # 將二維陣列轉為一維，方便計算總共有幾個 'X'
#     flat_board = [item for row in board for item in row]
#     logger.info(f"扁平化後的棋盤: {flat_board}")
    
#     if __name__ == "__main__":
#         logger.info("=== 開始 Python List 學習紀錄 ===")
    
#         demo_slicing_and_indexing()
#         demo_concatenation()
#         demo_mutability_and_replacement()
#         demo_nested_lists()
    
#         logger.info("=== 結束紀錄 ===")