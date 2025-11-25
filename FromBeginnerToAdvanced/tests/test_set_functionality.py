# source .venv/bin/activate
# uv pip install pytest
import pytest

# ----------------------------------------------------------------
# 類別一：內容修改與管理 (Modification)
# ----------------------------------------------------------------

def test_set_modification_methods():
    """
    測試 Set 的新增、刪除和清空功能。
    """
    my_set = {"Apple", "Banana"}

    # 1. add() - 新增單一元素
    my_set.add("Cherry")
    assert "Cherry" in my_set
    assert len(my_set) == 3

    # 2. update() - 新增多個元素 (使用列表)
    my_set.update(["Date", "Fig"])
    assert "Date" in my_set and "Fig" in my_set
    assert len(my_set) == 5

    # 3. discard() - 刪除存在的元素 (安全刪除)
    # my_set.discard("Apple----")    
    my_set.discard("Apple")
    assert "Apple" not in my_set

    # 4. discard() - 嘗試刪除不存在的元素 (不會報錯)
    my_set.discard("Grape")
    assert len(my_set) == 4 # 長度不變

    # 5. remove() - 刪除存在的元素
    my_set.remove("Banana")
    assert "Banana" not in my_set

    # 6. pop() - 隨機移除一個元素
    popped_item = my_set.pop()
    assert popped_item not in my_set
    assert len(my_set) == 2

    # 7. clear() - 清空 Set
    my_set.clear()
    assert len(my_set) == 0
    assert my_set == set()


def test_remove_raises_keyerror():
    """
    測試 remove() 在元素不存在時會引發 KeyError。
    """
    test_set = {1, 2}
    # 預期當嘗試移除不存在的元素 99 時，會拋出 KeyError
    with pytest.raises(KeyError):
        test_set.remove(99) # 沒出錯，騙人
        #   test_set.discard(99) # <-- 這裡使用 discard()
        # 


# ----------------------------------------------------------------
# 類別二：高效的集合運算 (Set Operations)
# ----------------------------------------------------------------

def test_set_operations_operators():
    """
    測試使用運算符進行集合運算 (聯集 |、交集 &、差集 -、對稱差集 ^)。
    """
    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}

    # 1. 聯集 (Union): A 或 B
    union_result = A | B
    assert union_result == {1, 2, 3, 4, 5, 6}

    # 2. 交集 (Intersection): A 且 B
    intersection_result = A & B
    assert intersection_result == {3, 4}

    # 3. 差集 (Difference): A 獨有
    difference_result = A - B
    assert difference_result == {1, 2}

    difference_result = B - A
    assert difference_result == {5, 6}

    # 4. 對稱差集 (Symmetric Difference): 互相獨有
    sym_diff_result = A ^ B
    assert sym_diff_result == {1, 2, 5, 6}


# ----------------------------------------------------------------
# 類別三：狀態查詢與比較 (Query and Comparison)
# ----------------------------------------------------------------

def test_set_query_and_comparison():
    """
    測試成員資格、子集、超集和不相交檢查。
    """
    set_parent = {10, 20, 30, 40}
    set_child = {10, 30}
    set_other = {50, 60}

    # 1. 成員資格測試 (in 運算符)
    assert 20 in set_parent
    assert 50 not in set_parent

    # 2. issubset() - 檢查是否為子集
    assert set_child.issubset(set_parent)
    assert not set_parent.issubset(set_child) # 父集不是子集

    # 3. issuperset() - 檢查是否為超集
    assert set_parent.issuperset(set_child)
    assert not set_child.issuperset(set_parent) # 子集不是超集

    # 4. isdisjoint() - 檢查是否不相交 (沒有共同元素)
    assert set_parent.isdisjoint(set_other)
    assert not set_parent.isdisjoint(set_child) # 有共同元素，所以不是不相交


# ----------------------------------------------------------------
# 類別四：高效的「原地」修改 (In-Place Updates)
# ----------------------------------------------------------------

def test_set_in_place_updates():
    """
    測試使用 *=, -=, &=, ^= 進行原地修改。
    """
    # 初始 Set
    set_original = {1, 2, 3, 4, 5}
    set_other = {4, 5, 6, 7}

    # 1. intersection_update (&=): 原地交集
    set_a = set_original.copy()
    set_a &= set_other
    assert set_a == {4, 5}

    # 2. difference_update (-=): 原地差集
    set_b = set_original.copy()
    set_b -= set_other
    assert set_b == {1, 2, 3}

    # 3. symmetric_difference_update (^=): 原地對稱差集
    set_c = set_original.copy()
    set_c ^= set_other
    assert set_c == {1, 2, 3, 6, 7}

    # 4. update (|=): 原地聯集 (等同於 update() 方法)
    set_d = {1, 2}
    set_d |= {3, 4}
    assert set_d == {1, 2, 3, 4}