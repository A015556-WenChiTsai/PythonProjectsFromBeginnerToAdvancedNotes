import curses
from curses import wrapper
import queue
import time
import logging

# 設定 Logging
logging.basicConfig(
    filename='maze_debug_set.log', # 修改 log 檔名以區分
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
    # 1. 開始計時
    start_time = time.time()
    
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    
    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    
    # ==========================================
    # 使用 Set (集合)
    # 搜尋速度: O(1) - 超級快，不管資料多少，速度幾乎一樣
    # ==========================================
    visited = set() 
    
    logging.info(f"=== [SET 版本] 程式開始 ===")
    
    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2) # 注意：這個 sleep 會佔據大部分的執行時間
        stdscr.refresh()

        if maze[row][col] == end:
            # 2. 結束計時
            end_time = time.time()
            duration = end_time - start_time
            logging.info(f"🎉 找到終點了！總耗時: {duration:.4f} 秒")
            # 在畫面上顯示時間
            stdscr.addstr(len(maze) + 1, 0, f"Time: {duration:.4f} sec (Set)")
            stdscr.refresh()
            return path

        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:
            if neighbor in visited: # Set 的查詢是 O(1)
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor) # Set 使用 add

    logging.info("=== 搜尋結束，無路可走 ===")

def find_neighbors(maze, row, col):
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))
    if row + 1 < len(maze): neighbors.append((row + 1, col))
    if col > 0: neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]): neighbors.append((row, col + 1))
    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)