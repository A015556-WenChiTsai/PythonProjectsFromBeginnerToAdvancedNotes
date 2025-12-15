import jieba
def jieba_tokenizer(text: str) -> list[str]:
    """使用 jieba 進行中文分詞和字元級別的標記化"""
    tokens: list[str] = []
    words: list[str] = list(jieba.cut(text))
    tokens.extend(words)

    # 為多字詞添加字元級別的標記
    for word in words:
        if len(word) > 1:
            tokens.extend(list(word))

    return tokens

jieba_tokenizer("我愛自然語言處理")

def jieba_tokenizer2(text: str) -> list[str]:
    """使用 jieba 進行中文分詞和字元級別的標記化"""
    words = list(jieba.cut(text))
    # Pythonic: 使用列表推導式展開字元
    char_tokens = [char for word in words if len(word) > 1 for char in word]
    return words + char_tokens

def test_basic_logic():
    text = "我愛自然語言處理"
    
    res1 = jieba_tokenizer(text)
    res2 = jieba_tokenizer2(text)
    
    print(f"Function 1 結果: {res1}")
    print(f"Function 2 結果: {res2}")
    
    # 測試兩個函式結果是否完全相同
    assert res1 == res2, "兩個函式的結果不一致！"
    
    # 測試預期結果 (手動驗證邏輯)
    # jieba 分詞預期: ['我', '愛', '自然語言處理']
    # 字元展開預期: ['自', '然', '語', '言', '處', '理']
    expected = ['我', '愛', '自然', '語言', '處理', '自', '然', '語', '言', '處', '理']
    assert res1 == expected, f"結果不符合預期，得到: {res1}"
    
    print("✅ 基礎邏輯測試通過！")

test_basic_logic()