import os
import shutil
import datetime
import schedule
import time
import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class AutomatedFileBackup:
    """自動化文件備份類別"""
    
    def __init__(self, source_dir: str, destination_dir: str):
        self.source_dir = Path(source_dir)
        self.destination_dir = Path(destination_dir)
        self.logger = self._setup_logger()
        
        # 確保目標目錄存在
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"初始化備份工具 - 來源: {self.source_dir}, 目標: {self.destination_dir}")
    
    def _setup_logger(self) -> logging.Logger:
        """設定 logger 配置"""
        logger = logging.getLogger('file_backup')
        logger.setLevel(logging.INFO)
        
        # 如果已經有 handler，就不重複添加
        if logger.handlers:
            return logger
        
        # 創建 logs 目錄
        log_dir = Path(__file__).parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # 控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 文件處理器 - 使用 RotatingFileHandler
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'backup.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def copy_folder_to_directory(self) -> bool:
        """
        複製資料夾到目標目錄
        
        Returns:
            bool: 備份是否成功
        """
        today = datetime.date.today()
        dest_dir = self.destination_dir / str(today)
        
        self.logger.info(f"開始備份程序 - 目標路徑: {dest_dir}")
        
        # 檢查來源目錄是否存在
        if not self.source_dir.exists():
            self.logger.error(f"來源目錄不存在: {self.source_dir}")
            return False
        
        # 如果目標目錄已存在，先刪除
        if dest_dir.exists():
            self.logger.warning(f"目標目錄已存在，將覆蓋: {dest_dir}")
            try:
                shutil.rmtree(dest_dir)
                self.logger.info(f"已刪除現有目錄: {dest_dir}")
            except Exception as e:
                self.logger.error(f"刪除現有目錄失敗: {e}")
                return False
        
        # 執行備份
        try:
            # 獲取來源目錄大小資訊
            total_size = self._get_directory_size(self.source_dir)
            self.logger.info(f"來源目錄大小: {self._format_size(total_size)}")
            
            start_time = time.time()
            shutil.copytree(self.source_dir, dest_dir)
            end_time = time.time()
            
            duration = end_time - start_time
            self.logger.info(f"備份完成! 目標路徑: {dest_dir}")
            self.logger.info(f"備份耗時: {duration:.2f} 秒")
            
            # 驗證備份完整性
            if self._validate_backup(dest_dir):
                self.logger.info("備份完整性驗證通過")
                return True
            else:
                self.logger.error("備份完整性驗證失敗")
                return False
                
        except FileExistsError:
            self.logger.warning(f"目錄已存在: {dest_dir}")
            return False
        except PermissionError as e:
            self.logger.error(f"權限錯誤: {e}")
            return False
        except Exception as e:
            self.logger.error(f"備份過程中發生錯誤: {e}")
            return False
    
    def _get_directory_size(self, path: Path) -> int:
        """計算目錄大小"""
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, FileNotFoundError):
                        # 忽略無法訪問的文件
                        continue
        except Exception as e:
            self.logger.warning(f"計算目錄大小時發生錯誤: {e}")
        
        return total_size
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    def _validate_backup(self, backup_path: Path) -> bool:
        """驗證備份的完整性"""
        try:
            # 簡單的驗證：檢查目錄是否存在且不為空
            if not backup_path.exists():
                return False
            
            # 計算文件數量
            source_files = sum(1 for _ in self.source_dir.rglob('*') if _.is_file())
            backup_files = sum(1 for _ in backup_path.rglob('*') if _.is_file())
            
            self.logger.debug(f"來源文件數: {source_files}, 備份文件數: {backup_files}")
            
            return source_files == backup_files
            
        except Exception as e:
            self.logger.error(f"驗證備份時發生錯誤: {e}")
            return False
    
    def setup_schedule(self, time_str: str = "18:57") -> None:
        """
        設定定時備份
        
        Args:
            time_str: 執行時間，格式為 "HH:MM"
        """
        self.logger.info(f"設定每日定時備份，執行時間: {time_str}")
        schedule.every().day.at(time_str).do(self.copy_folder_to_directory)
    
    def run_scheduler(self) -> None:
        """運行排程器"""
        self.logger.info("排程器開始運行... (按 Ctrl+C 結束)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("收到中斷信號，正在停止排程器...")
        except Exception as e:
            self.logger.error(f"排程器運行時發生錯誤: {e}")
        finally:
            self.logger.info("排程器已停止")


def main():
    """主函數"""
    # 設定路徑
    source_dir = "/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced"
    destination_dir = "/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/Backups"
    
    # 創建備份實例
    backup_manager = AutomatedFileBackup(source_dir, destination_dir)
    
    # 立即執行一次備份來測試功能
    print("開始執行備份測試...")
    success = backup_manager.copy_folder_to_directory()
    
    if success:
        print("✓ 備份測試成功完成")
    else:
        print("✗ 備份測試失敗")
        return
    
    # 設定定時備份
    backup_manager.setup_schedule("18:57")
    
    # 運行排程器
    backup_manager.run_scheduler()


if __name__ == "__main__":
    main()
