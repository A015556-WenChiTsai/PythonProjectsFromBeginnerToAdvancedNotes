import os
import shutil
import datetime
import schedule
import time

source_dir = "/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced"
destination_dir = "/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/Backups"

def copy_folder_to_directory(source, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))
    
    try:
        shutil.copytree(source, dest_dir)
        print(f"Folder copied to: {dest_dir}")
    except FileExistsError:
        print(f"Folder already exists in: {dest}")


# 立即執行一次備份來測試功能
print("開始執行備份測試...")
copy_folder_to_directory(source_dir, destination_dir)

# 設定每天下午 6:57 自動備份
schedule.every().day.at("18:57").do(lambda: copy_folder_to_directory(source_dir, destination_dir))

print("自動備份已設定，每天下午 6:57 執行")
print("程式正在運行中... (按 Ctrl+C 結束)")

while True:
    schedule.run_pending()
    time.sleep(60)