import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    print(f"check_winnings columns:{columns} ,lines:{lines} ,bet:{bet} ,values:{values}")
    winnings = 0
    winning_lines = []
    for line in range(lines):
        # print(f"正在檢查第 {line + 1} 線")
        symbol = columns[0][line]
        # print(f"符號為 {symbol} 的第 {line + 1} 線")
        for column in columns:
            # print(f"column[line]: {column[line]}")
            symbol_to_check = column[line]
            # print(f"symbol_to_check: {symbol_to_check}")
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
                               
    print(f"all_symbols: {all_symbols}")

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    print("print_slot_machine:",columns)
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()


def deposit():
    while True:
        amount = input("您想存入多少錢？ $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("金額必須大於 0。")
        else:
            print("請輸入一個數字。")

    return amount


def get_number_of_lines():
    while True:
        lines = input(
            "您想在多少條線上下注？ (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("請輸入有效的線數。")
        else:
            print("請輸入一個數字。")

    return lines


def get_bet():
    while True:
        amount = input("您想在每條線上下注多少錢？ $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"金額必須在 ${MIN_BET} - ${MAX_BET} 之間。")
        else:
            print("請輸入一個數字。")

    return amount


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"您的餘額不足以下注該金額，您目前的餘額是: ${balance}")
        else:
            break

    print(
        f"您在 {lines} 條線上下注 ${bet}。總下注金額為: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"您贏得了 ${winnings}。")
    print(f"您在以下線上贏得獎金:", *winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"當前餘額為 ${balance}")
        answer = input("按回車鍵開始遊戲 (輸入 q 退出)。")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"您離開時的餘額為 ${balance}")


main()