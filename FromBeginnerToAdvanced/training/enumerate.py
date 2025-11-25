def get_indexed_items(data):
    """使用 enumerate 獲取標準 0-based 索引和值。"""
    # 注意：enumerate 返回一個生成器，我們通常需要將其轉換為 list 或在 for 迴圈中使用
    return list(enumerate(data))

items = ['Apple', 'Banana', 'Cherry']
print(get_indexed_items(items))
def create_human_readable_list(data, start_num=1):
    """使用 start 參數，生成一個從 1 或指定數字開始的清單。"""
    results = []
    # 關鍵：傳入 start=start_num
    for rank, item in enumerate(data, start=start_num):
        results.append(f"第 {rank} 項: {item}")
    return results    
data = ['A', 'B']

print(create_human_readable_list(data, start_num=100))
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

student_scores = [55, 40, 75, 90, 60]
print(find_first_passing_student_position(student_scores, threshold=70))
student_scores = [55, 40, 65, 59]
print(find_first_passing_student_position(student_scores, threshold=80))