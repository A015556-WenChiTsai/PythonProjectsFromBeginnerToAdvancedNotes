print("歡迎來的到Python練習！ ")
playing=input ("隨便輸入文字 ")
if playing.lower() != "yes" :
    quit()

# 大寫
# if playing.upper() != "YES" :    
#     quit()
#number_quesser
score=0
print("太好了！讓我們開始吧！ ")
answer = input("你知道CPU是什麼嗎? ")
if answer == "中央處理器":
    print("正確！ ")
    score+=1
else:
    print("錯誤！答案是中央處理器 ")    
    
print("你的得分是 " + str(score))    