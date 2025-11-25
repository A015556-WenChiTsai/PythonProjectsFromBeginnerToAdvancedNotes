with open("FromBeginnerToAdvanced/story.txt", "r") as f:
    story = f.read()
    print(story)

#
words = set()#如果建立時出現重複的項目，只會保留一個，如果是字典，只會保留鍵，如果是布林，True 等同 1，False 等同 0。
start_of_word = -1

target_start = "<"
target_end = ">"

seasons = [ 'Spring' , 'Summer' , 'Fall' , 'Winter' ]
enumerate(seasons, start=9)
print(f'enumerate 9:{list(enumerate(seasons, start=9))}')#:[(9, 'Spring'), (10, 'Summer'), (11, 'Fall'), (12, 'Winter')]
a1=list ( enumerate ( seasons ) )#[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
print(f'enumerate:{a1}')
aaa = list(enumerate(story))#[(0, 'I'), (1, 'n'), (2, ' '), (3, 't')...
print(f'enumerate:{aaa}')
for i, char in enumerate(story):    
    if char == target_start:
        # print(char)
        start_of_word = i
        print("start_of_word:", start_of_word)

    if char == target_end and start_of_word != -1:
        word = story[start_of_word: i + 1]
        words.add(word)
        print("--- 偵測到的所有填空詞2 (words) ---")
        print(words)
        start_of_word = -1
        
# =================================================
# 在這裡加入 print 語句
print("--- 偵測到的所有填空詞 (words) ---")
print(words)
print("------------------------------------")
# =================================================        

answers = {}

for word in words:
    answer = input("請輸入一個詞語來替換 " + word + ": ")
    answers[word] = answer

for word in words:
    story = story.replace(word, answers[word])

print(story)