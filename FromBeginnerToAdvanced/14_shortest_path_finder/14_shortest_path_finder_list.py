import curses
from curses import wrapper
import queue
import time
import logging

# 設定 Logging
logging.basicConfig(
    filename='maze_debug_list.log', # 修改 log 檔名以區分
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
    # 使用 List (列表)
    # 搜尋速度: O(N) - 資料越多，檢查越慢
    # ==========================================
    visited = [] 
    
    logging.info(f"=== [LIST 版本] 程式開始 ===")
    
    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2) 
        stdscr.refresh()

        if maze[row][col] == end:
            # 2. 結束計時
            end_time = time.time()
            duration = end_time - start_time
            logging.info(f"🎉 找到終點了！總耗時: {duration:.4f} 秒")
            stdscr.addstr(len(maze) + 1, 0, f"Time: {duration:.4f} sec (List)")
            stdscr.refresh()
            return path

        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:
            # 這裡就是效能瓶頸！
            # List 必須從頭到尾檢查每一個元素，看 neighbor 是否在裡面
            if neighbor in visited: 
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            
            # List 使用 append
            visited.append(neighbor) 

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