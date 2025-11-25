# adventure_game.py

def start_game():
    """
    遊戲的起始點。
    """
    print("--- 歡迎來到迷霧森林的邊緣 ---")
    print("你醒來時發現自己身處一片濃霧籠罩的森林邊緣。")
    print("你不知道自己是誰，也不知道如何來到這裡。")
    print("在你面前有兩條路：")
    print("1. 一條通往森林深處的泥濘小徑。")
    print("2. 一條沿著山腳延伸的崎嶇石路。")
    
    choice = input("你會選擇哪條路？ (輸入 1 或 2): ")
    
    if choice == '1':
        forest_path()
    elif choice == '2':
        mountain_path()
    else:
        print("輸入無效。遊戲結束。")

def forest_path():
    """
    森林小徑的分支。
    """
    print("\n你選擇了泥濘的小徑，濃霧讓你幾乎看不清腳下的路。")
    print("走了不久，你聽到遠處傳來微弱的呼救聲。")
    print("你必須決定：")
    print("1. 忽略聲音，繼續沿著小徑前進。")
    print("2. 離開小徑，朝著聲音的方向深入森林。")
    
    choice = input("你會怎麼做？ (輸入 1 或 2): ")
    
    if choice == '1':
        print("\n你繼續前進，但濃霧越來越厚，你最終迷失了方向。")
        print("你筋疲力盡，倒在地上，再也沒有醒來。")
        end_game("迷失在濃霧中")
    elif choice == '2':
        rescue_attempt()
    else:
        print("輸入無效。遊戲結束。")

def rescue_attempt():
    """
    嘗試救援的分支。
    """
    print("\n你勇敢地朝著呼救聲前進。你發現一個被藤蔓纏住的古老寶箱。")
    print("呼救聲似乎是從寶箱裡傳出來的。")
    print("你必須決定：")
    print("1. 嘗試打開寶箱。")
    print("2. 認為這是陷阱，轉身離開。")
    
    choice = input("你會怎麼做？ (輸入 1 或 2): ")
    
    if choice == '1':
        print("\n你費力地打開了寶箱。裡面沒有人，只有一塊閃閃發光的魔法石。")
        print("當你拿起魔法石時，濃霧瞬間消散，你發現自己站在一座宏偉城堡的門口。")
        end_game("獲得魔法石，抵達城堡", win=True)
    elif choice == '2':
        print("\n你轉身離開，但當你回到小徑時，你發現小徑已經消失了。")
        print("你被困在森林裡，最終被野獸吞噬。")
        end_game("被困與被吞噬")
    else:
        print("輸入無效。遊戲結束。")

def mountain_path():
    """
    崎嶇石路的分支。
    """
    print("\n你選擇了崎嶇的石路。這條路通往一座陡峭的山峰。")
    print("你爬了很久，口渴難耐。你看到路邊有一個清澈的小水潭。")
    print("你必須決定：")
    print("1. 立即飲用潭水解渴。")
    print("2. 忍住口渴，繼續向上爬。")
    
    choice = input("你會怎麼做？ (輸入 1 或 2): ")
    
    if choice == '1':
        print("\n你喝下了潭水。水很甜美，但幾秒鐘後，你感到全身麻痺。")
        print("這水有毒！你倒在地上，意識漸漸模糊。")
        end_game("中毒身亡")
    elif choice == '2':
        summit_reach()
    else:
        print("輸入無效。遊戲結束。")

def summit_reach():
    """
    到達山頂的分支。
    """
    print("\n你忍住了口渴，繼續向上爬。終於，你到達了山頂。")
    print("在山頂上，你看到一個古老的祭壇，上面放著一把生鏽的鑰匙。")
    print("你必須決定：")
    print("1. 拿起鑰匙。")
    print("2. 離開，尋找下山的路。")
    
    choice = input("你會怎麼做？ (輸入 1 或 2): ")
    
    if choice == '1':
        print("\n你拿起了鑰匙。突然，一隻巨大的石像鬼從天而降，將你抓走。")
        end_game("被石像鬼抓走")
    elif choice == '2':
        print("\n你決定下山。在下山的路上，你遇到了一隊友善的旅人。")
        print("他們帶你回到了文明世界，你開始了新的生活。")
        end_game("安全返回文明世界", win=True)
    else:
        print("輸入無效。遊戲結束。")

def end_game(ending_message, win=False):
    """
    顯示遊戲結局並結束程式。
    """
    print("\n" + "="*30)
    if win:
        print("【勝利結局】")
    else:
        print("【失敗結局】")
    print(f"結局描述: {ending_message}")
    print("遊戲結束。")
    print("="*30)

# 程式主入口
if __name__ == "__main__":
    start_game()