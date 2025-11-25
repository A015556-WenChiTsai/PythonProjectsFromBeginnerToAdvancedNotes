# my_set=set()
# my_set = {"Apple", "Banana"}
#     # 1. add() - 新增單一元素
# my_set.add("Cherry")
# print(f'my_set 1: {my_set}')
# my_set.update(["Date", "Fig"])
# print(f'my_set 2: {my_set}')
# my_set.discard("Apple")
# print(f'my_set 3: {my_set}')
# my_set.discard("aaa")
# print(f'my_set 4: {my_set}')
# my_set.clear()
# print(f'my_set 5: {my_set}')

# test_set = {1, 2}
# test_set.discard(99)
# print(f'my_set 6: {test_set}')
# test_set.remove(99)
# print(f'my_set 7: {test_set}')
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
# 1. 聯集 (Union): A 或 B
union_result = A | B
print(f'union_result: {union_result}')
# 2. 交集 (Intersection): A 且 B
intersection_result = A & B
print(f'intersection_result: {intersection_result}')
# 3. 差集 (Difference): A 非 B
difference_result = A - B
print(f'difference_result A 非 B: {difference_result}')
difference_result = B - A
print(f'difference_result B 非 A: {difference_result}')
sym_diff_result = A ^ B
print(f'sym_diff_result A ^ B 【對稱差集 (Symmetric Difference): 互相獨有】: {sym_diff_result}')

set_parent = {10, 20, 30, 40}
set_child = {10, 30}
set_other = {50, 60}
print(f'20 in set_parent: {20 in set_parent}')
print(f'50 not in set_parent: {50 not in set_parent}')
print(f'set_child is subset of set_parent: {set_child.issubset(set_parent)}')#set_child 是否為 set_parent 的子集
print(f'set_parent is subset of set_child: {set_parent.issubset(set_child)}')#set_parent 是否為 set_child 的子集
print(f'set_parent is superset of set_child: {set_parent.issuperset(set_child)}')#set_child 是否為 set_parent 的一部分
print(f'set_child is superset of set_parent: {set_child.issuperset(set_parent)}')#set_parent 是否為 set_child 的一部分