import random

COLORS = ["R", "G", "B", "Y", "O", "P"]
TRIES = 10
CODE_LENGTH = 4

def generate_code():
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]
def guess_code():
    while True:
        guess = input(
            f"輸入你的猜測 ({CODE_LENGTH} 個字母，必須是以下顏色之一：{', '.join(COLORS)}): "
        ).upper()
        if len(guess) != CODE_LENGTH or any(c not in COLORS for c in guess):
            print(
                f"無效的輸入。請輸入正好 {CODE_LENGTH} 個字母，且必須是以下顏色之一：{', '.join(COLORS)}。"
            )
        else:
            return list(guess)


def evaluate_guess(code, guess):
    correct_position = sum(c == g for c, g in zip(code, guess))
    correct_color = (
        sum(min(code.count(c), guess.count(c)) for c in set(COLORS)) - correct_position
    )
    return correct_position, correct_color


def main():
    print("歡迎來到大師班！")
    code = generate_code()
    for attempt in range(1, TRIES + 1):
        print(f"嘗試次數 {attempt} / {TRIES}")
        guess = guess_code()
        correct_position, correct_color = evaluate_guess(code, guess)
        if correct_position == CODE_LENGTH:
            print(f"恭喜你！你猜對了密碼：{''.join(code)}")
            break
        else:
            print(f"正確顏色且位置正確的數量: {correct_position}")
            print(f"正確顏色但位置錯誤的數量: {correct_color}")
    else:
        print(f"很遺憾，你已經用完所有嘗試次數。密碼是：{''.join(code)}")


if __name__ == "__main__":
    main()
