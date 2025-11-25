# 函數：將列表轉換為 (索引, 值) 的元組列表
def get_indexed_items(data):
    """使用 enumerate 獲取標準 0-based 索引和值。"""
    # 注意：enumerate 返回一個生成器，我們通常需要將其轉換為 list 或在 for 迴圈中使用
    return list(enumerate(data))
def test_basic_zero_indexing():
    """測試 enumerate 預設從 0 開始計數。"""
    items = ['Apple', 'Banana', 'Cherry']
    
    # 預期結果：(0, 'Apple'), (1, 'Banana'), (2, 'Cherry')
    expected = [(0, 'Apple'), (1, 'Banana'), (2, 'Cherry')]
    
    assert get_indexed_items(items) == expected
# 函數：生成一個從指定數字開始編號的清單
def create_human_readable_list(data, start_num=1):
    """使用 start 參數，生成一個從 1 或指定數字開始的清單。"""
    results = []
    # 關鍵：傳入 start=start_num
    for rank, item in enumerate(data, start=start_num):
        results.append(f"第 {rank} 項: {item}")
    return results    

def test_one_based_indexing_start_parameter():
    """測試 enumerate 的 start 參數，確保編號從 1 開始。"""
    shopping_list = ['牛奶', '雞蛋', '麵包']
    
    # 預期結果：從 1 開始
    expected = [
        '第 1 項: 牛奶', 
        '第 2 項: 雞蛋', 
        '第 3 項: 麵包'
    ]
    
    assert create_human_readable_list(shopping_list, start_num=1) == expected

def test_custom_start_value():
    """測試 start 參數可以從任意數字開始。"""
    data = ['A', 'B']
    # 讓編號從 100 開始
    expected = ['第 100 項: A', '第 101 項: B']
    
    assert create_human_readable_list(data, start_num=100) == expected
    
# 函數：找出第一個超過門檻值的成績的位置
def find_first_passing_student_position(scores, threshold=60):
    """
    遍歷成績列表，找出第一個超過門檻值的學生的索引。
    如果找到，返回 (索引, 成績)；否則返回 None。
    """
    for index, score in enumerate(scores):
        if score >= threshold:
            # 找到後立即返回，避免不必要的遍歷
            return index, score
            
    return None

def test_conditional_break_and_positioning():
    """測試 enumerate 用於條件判斷，並返回第一個符合條件的索引。"""
    
    # 數據：第 0, 1, 2, 3, 4 位學生
    student_scores = [55, 40, 75, 90, 60]
    
    # 門檻值設為 70 分
    threshold = 70
    
    # 預期結果：第一個超過 70 分的是 75 分，位於索引 2
    result = find_first_passing_student_position(student_scores, threshold=70)
    
    # 斷言：確保返回的索引是 2，成績是 75
    assert result == (2, 75)

def test_conditional_no_match():
    """測試當列表中沒有符合條件的元素時的行為。"""
    
    student_scores = [55, 40, 65, 59]
    
    # 門檻值設為 80 分
    result = find_first_passing_student_position(student_scores, threshold=80)
    
    # 斷言：確保返回 None
    assert result is None    