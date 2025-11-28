# carlos_nnb_ubuntu@LAPTOP-1O97PFDL:~/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced/21_advanced_python_scripting$ 
#python 21_advanced_python_scripting_2.py source_games target_games

# 驗證結果
# (.venv) carlos_nnb_ubuntu@LAPTOP-1O97PFDL:~/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced/21_advanced_python_scripting$ ./target_games/pong/main
# 這是 Pong Game！

# 驗證結果
# (.venv) carlos_nnb_ubuntu@LAPTOP-1O97PFDL:~/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced/21_advanced_python_scripting$ ./target_games/snake/game
# 這是 Snake Game！
import json
import shutil
import sys
import logging
from pathlib import Path
from subprocess import run, PIPE, CalledProcessError
from typing import List

# --- 配置設定 ---
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]
LOG_FILE = "build_process.log"

# --- Logging 設定 ---
def setup_logging():
    """設定日誌系統，同時輸出到控制台與檔案"""
    # 建立 Logger
    logger = logging.getLogger("GameBuilder")
    logger.setLevel(logging.INFO)

    # 格式設定
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 1. 檔案輸出 (File Handler)
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. 控制台輸出 (Stream Handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()

# --- 核心邏輯 ---

def find_all_game_paths(source: Path) -> List[Path]:
    """在來源目錄中尋找包含特定關鍵字的遊戲目錄"""
    game_paths = []
    
    # 使用 pathlib 的 iterdir() 比 os.walk 更直觀
    if not source.exists():
        logger.error(f"來源目錄不存在: {source}")
        return []
    
    #.iterdir()：這是 "Iterate Directory"（遍歷目錄）的縮寫。
    logger.info(f"source.iterdir:{list(source.iterdir())}")
    for item in source.iterdir():
        if item.is_dir() and GAME_DIR_PATTERN in item.name.lower():
            game_paths.append(item)
    logger.info(f"game_paths:{game_paths}")
    return game_paths


def get_name_from_paths(paths: List[Path], to_strip: str) -> List[str]:
    """從路徑中提取目錄名稱並移除指定字串"""
    new_names = []
    for path in paths:
        # pathlib 的 .name 屬性直接取得目錄名
        new_dir_name = path.name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names


def create_dir(path: Path):
    """建立目錄，如果已存在則忽略"""
    # exist_ok=True 是 Pythonic 的寫法，不需要先檢查是否存在
    # parents=True：自動建立父目錄
    # 這樣可以確保即使上層目錄不存在也能建立
    path.mkdir(parents=True, exist_ok=True)


def copy_and_overwrite(source: Path, dest: Path):
    """複製目錄，如果目標已存在則先刪除"""
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    logger.info(f"已複製: {source} -> {dest}")


def make_json_metadata_file(path: Path, game_dirs: List[str]):
    """建立包含遊戲資訊的 JSON 檔案"""
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4) # indent 讓 json 更易讀
        logger.info(f"Metadata 已寫入: {path}")
    except IOError as e:
        logger.error(f"寫入 Metadata 失敗: {e}")


def compile_game_code(path: Path):
    """尋找並編譯 Go 程式碼"""
    code_file = None
    
    # 使用 glob 尋找檔案，比 os.walk 簡潔
    for file in path.glob(f"*{GAME_CODE_EXTENSION}"):
        code_file = file
        break # 找到第一個就停止

    if code_file is None:
        logger.warning(f"在 {path} 中找不到 {GAME_CODE_EXTENSION} 檔案，跳過編譯。")
        return

    command = GAME_COMPILE_COMMAND + [code_file.name]
    run_command(command, path)


def run_command(command: List[str], cwd: Path):
    """執行系統命令"""
    try:
        # 使用 cwd 參數指定執行目錄，而不是用 os.chdir 切換全域目錄
        # check=True 會在命令失敗時拋出異常
        result = run(command, cwd=cwd, stdout=PIPE, stderr=PIPE, universal_newlines=True, check=True)
        logger.info(f"編譯成功 [{cwd.name}]: {result.stdout.strip() if result.stdout else '無輸出'}")
    
    except CalledProcessError as e:
        logger.error(f"編譯失敗 [{cwd.name}]: {e.stderr}")
    except Exception as e:
        logger.error(f"執行命令時發生未預期錯誤: {e}")


def main(source: str, target: str):
    cwd = Path.cwd()
    logger.info(f"當前工作目錄:{cwd}")
    source_path = cwd / source # pathlib 的路徑拼接寫法
    target_path = cwd / target

    logger.info(f"開始處理... 來源: {source_path}, 目標: {target_path}")

    game_paths = find_all_game_paths(source_path)
    if not game_paths:
        logger.warning("未找到任何遊戲目錄，程式結束。")
        return

    new_game_dirs = get_name_from_paths(game_paths, "_game")

    create_dir(target_path)

    # 使用 zip 同時遍歷來源路徑和新目錄名稱
    for src, dest_name in zip(game_paths, new_game_dirs):
        dest_path = target_path / dest_name
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = target_path / "metadata.json"
    make_json_metadata_file(json_path, new_game_dirs)
    
    logger.info("所有作業已完成！")


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("錯誤：您必須提供原始目錄 (source) 和目標目錄 (target)。")
        print(f"用法範例：python {Path(__file__).name} source_games target_games")
        sys.exit(1)

    source_dir, target_dir = args[1:]
    #python 21_advanced_python_scripting.py source_games target_games
    # 索引 (Index)	內容 (Value)	意義
    # args[0]	'21_advanced_python_scripting.py'	程式腳本本身的名稱 (我們通常不需要處理這個)
    # args[1]	'source_games'	第一個參數 (你的來源目錄)
    # args[2]	'target_games'	第二個參數 (你的目標目錄)
    # 所以 args[1:] 的意思就是：「給我這個列表中，從第 2 個元素開始，直到最後的所有元素。」 (也就是把第 1 個元素 args[0] 丟掉)。
    # 原始列表 args:
#     [ 'script.py', 'source_games', 'target_games' ]
#       ↑              ↑               ↑
#    索引 0          索引 1           索引 2
#   (不要這個)      (我要從這裡開始......到最後)

#     執行 args[1:] 之後的結果:
#     [ 'source_games', 'target_games' ]
    main(source_dir, target_dir)