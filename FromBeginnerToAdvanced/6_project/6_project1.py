import random


def roll():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)

    return roll


while True:
    players = input("請輸入玩家人數（2-4人）： ")
    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("玩家人數必須介於2到4人之間。")
    else:
        print("輸入無效，請再試一次。")

max_score = 50
player_scores = [0 for _ in range(players)]

while max(player_scores) < max_score:
    for player_idx in range(players):
        print("\n玩家", player_idx + 1, "的回合開始了！")
        print("你的總分是:", player_scores[player_idx], "\n")
        current_score = 0

        while True:
            should_roll = input("你想擲骰子嗎（y）？ ")
            if should_roll.lower() != "y":
                break

            value = roll()
            if value == 1:
                print("你擲出了1！回合結束！")
                current_score = 0
                break
            else:
                current_score += value
                print("你擲出了:", value)

            print("你的分數是:", current_score)

        player_scores[player_idx] += current_score
        print("你的總分是:", player_scores[player_idx])

max_score = max(player_scores)
winning_idx = player_scores.index(max_score)
print("球員號碼", winning_idx + 1,
      "是贏家，得分為:", max_score)