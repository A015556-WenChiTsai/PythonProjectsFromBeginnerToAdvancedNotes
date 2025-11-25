import turtle
import time
import random

WIDTH, HEIGHT = 700, 600
COLORS = ['紅色', '綠色', '藍色', '橙色', '黃色', '黑色', '紫色', '粉色', '棕色', '青色']
COLOR_MAP = {
    '紅色': 'red',
    '綠色': 'green',
    '藍色': 'blue',
    '橙色': 'orange',
    '黃色': 'yellow',
    '黑色': 'black',
    '紫色': 'purple',
    '粉色': 'pink',
    '棕色': 'brown',
    '青色': 'cyan'
}

def get_number_of_racers():
	racers = 0
	while True:
		racers = input('請輸入參賽者數量 (2 - 10): ')
		if racers.isdigit():
			racers = int(racers)
		else:
			print('輸入不是數字... 請再試一次!')
			continue

		if 2 <= racers <= 10:
			return racers
		else:
			print('數字不在範圍 2-10 內。請再試一次!')

def race(colors):
	turtles = create_turtles(colors)

	while True:
		for racer in turtles:
			distance = random.randrange(1, 20)
			racer.forward(distance)

			x, y = racer.pos()
			if y >= HEIGHT // 2 - 10:
				return colors[turtles.index(racer)]

def create_turtles(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
		# 獲取 turtle 能夠識別的英文顏色名稱
        english_color = COLOR_MAP.get(color, 'black') # 如果找不到，預設為黑色
        racer = turtle.Turtle()
		# 3. 使用英文名稱設定顏色
        racer.color(english_color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20)
        racer.pendown()
        turtles.append(racer)

    return turtles

# def create_turtles(colors):
# 	turtles = []
# 	spacingx = WIDTH // (len(colors) + 1)
# 	for i, color in enumerate(colors):
# 		racer = turtle.Turtle()
# 		racer.color(color)
# 		racer.shape('turtle')
# 		racer.left(90)
# 		racer.penup()
# 		racer.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20)
# 		racer.pendown()
# 		turtles.append(racer)

# 	return turtles

def init_turtle():
	screen = turtle.Screen()
	screen.setup(WIDTH, HEIGHT)
	screen.title('烏龜賽跑!')

racers = get_number_of_racers()
init_turtle()

print("參賽的顏色有:", COLORS)
random.shuffle(COLORS)
colors = COLORS[:racers]

print("參賽的顏色有:", colors)
winner = race(colors)
print("獲勝的是顏色為:", winner, "的烏龜")
time.sleep(5)