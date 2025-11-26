import curses
from curses import wrapper
import queue
import time
import logging  # 1. 引入 logging 模組

# ==========================================
# 設定 Logging (寫入到 maze_debug.log 檔案)
# filemode='w' 代表每次執行都會清空舊的 log，重新寫入
# ==========================================
logging.basicConfig(
    filename='maze_debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S',
    filemode='w' 
)

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    logging.info(f"start_pos: {start_pos}")
    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set()# 為什麼用set，因為O(1):
    logging.info(f"visited 1: {visited}")
    #O(1):常數時間
    
    # 記錄開始
    logging.info(f"=== 程式開始 ===")
    logging.info(f"起點座標: {start_pos}")

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        # 記錄當前處理的節點
        logging.info(f"--------------------------------")
        logging.info(f"📍 目前位置: {current_pos}")
        logging.info(f"   目前路徑長度: {len(path)}")

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            logging.info(f"🎉 找到終點了！路徑: {path}")
            return path

        neighbors = find_neighbors(maze, row, col)
        logging.info(f"   🔍 找到鄰居: {neighbors}")

        for neighbor in neighbors:
            logging.info(f"visited 2: {visited}")
            if neighbor in visited:
                logging.info(f"      ❌ 鄰居 {neighbor} 已經走過 (Visited)，跳過")
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                logging.info(f"      🧱 鄰居 {neighbor} 是牆壁，跳過")
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)
            logging.info(f"      ✅ 加入鄰居 {neighbor} 到 Queue 中等待探索")

    logging.info("=== 搜尋結束，無路可走 ===")


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()


wrapper(main)