import os
import shutil
import datetime
import schedule
import time
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Protocol, Dict, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum


# ===== 資料模型 =====
@dataclass
class BackupResult:
    """備份結果資料模型"""
    success: bool
    message: str
    source_path: Path
    destination_path: Optional[Path] = None
    duration: Optional[float] = None
    file_count: Optional[int] = None
    total_size: Optional[int] = None


@dataclass
class BackupConfiguration:
    """備份配置資料模型"""
    source_dir: Union[str, Path]
    destination_dir: Union[str, Path]
    schedule_time: str = "18:57"
    max_log_size: int = field(default=5 * 1024 * 1024)  # 5MB
    log_backup_count: int = 5
    enable_validation: bool = True
    
    def __post_init__(self):
        """後處理：確保路徑是 Path 物件"""
        self.source_dir = Path(self.source_dir)
        self.destination_dir = Path(self.destination_dir)


class LogLevel(Enum):
    """日誌級別枚舉"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# ===== 介面定義 =====
class ILogger(Protocol):
    """日誌介面"""
    
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...
    def critical(self, message: str) -> None: ...


class IFileOperations(Protocol):
    """文件操作介面"""
    
    def copy_directory(self, source: Path, destination: Path) -> bool: ...
    def delete_directory(self, path: Path) -> bool: ...
    def get_directory_size(self, path: Path) -> int: ...
    def count_files(self, path: Path) -> int: ...
    def directory_exists(self, path: Path) -> bool: ...


class IScheduler(Protocol):
    """排程器介面"""
    
    def schedule_daily(self, time_str: str, job_func: Callable[[], Any]) -> None: ...
    def run_pending(self) -> None: ...
    def clear_all(self) -> None: ...


class IBackupValidator(Protocol):
    """備份驗證器介面"""
    
    def validate(self, source: Path, backup: Path) -> bool: ...


class IBackupService(Protocol):
    """備份服務介面"""
    
    def backup(self) -> BackupResult: ...
    def setup_schedule(self, time_str: str) -> None: ...
    def run_scheduler(self) -> None: ...


# ===== 實作類別 =====
class FileLogger:
    """文件日誌記錄器實作"""
    
    def __init__(self, log_dir: Union[str, Path], max_bytes: int = 5*1024*1024, backup_count: int = 5):
        self.log_dir = Path(log_dir)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._logger: Optional[logging.Logger] = None
    
    @property
    def logger(self) -> logging.Logger:
        """延遲初始化 logger"""
        if self._logger is None:
            self._logger = self._setup_logger()
        return self._logger
    
    def _setup_logger(self) -> logging.Logger:
        """設定 logger 配置"""
        logger = logging.getLogger('file_backup_di')
        logger.setLevel(logging.INFO)
        
        # 如果已經有 handler，就不重複添加
        if logger.handlers:
            return logger
        
        # 創建 logs 目錄
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
        # 控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 文件處理器 - 使用 RotatingFileHandler
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'backup_di.log',
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
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
    
    def debug(self, message: str) -> None:
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        self.logger.critical(message)


class FileOperations:
    """文件操作實作"""
    
    def __init__(self, logger: ILogger):
        self.logger = logger
    
    def copy_directory(self, source: Path, destination: Path) -> bool:
        """複製目錄"""
        try:
            self.logger.info(f"開始複製目錄: {source} -> {destination}")
            shutil.copytree(source, destination)
            self.logger.info(f"目錄複製完成: {destination}")
            return True
        except Exception as e:
            self.logger.error(f"複製目錄失敗: {e}")
            return False
    
    def delete_directory(self, path: Path) -> bool:
        """刪除目錄"""
        try:
            if path.exists():
                self.logger.info(f"刪除目錄: {path}")
                shutil.rmtree(path)
                return True
            return True
        except Exception as e:
            self.logger.error(f"刪除目錄失敗: {e}")
            return False
    
    def get_directory_size(self, path: Path) -> int:
        """計算目錄大小"""
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, FileNotFoundError):
                        continue
            self.logger.debug(f"目錄 {path} 大小: {self._format_size(total_size)}")
        except Exception as e:
            self.logger.warning(f"計算目錄大小時發生錯誤: {e}")
        
        return total_size
    
    def count_files(self, path: Path) -> int:
        """計算文件數量"""
        try:
            count = sum(1 for _ in path.rglob('*') if _.is_file())
            self.logger.debug(f"目錄 {path} 文件數量: {count}")
            return count
        except Exception as e:
            self.logger.warning(f"計算文件數量時發生錯誤: {e}")
            return 0
    
    def directory_exists(self, path: Path) -> bool:
        """檢查目錄是否存在"""
        return path.exists() and path.is_dir()
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"


class ScheduleWrapper:
    """排程器包裝器"""
    
    def __init__(self, logger: ILogger):
        self.logger = logger
    
    def schedule_daily(self, time_str: str, job_func: Callable[[], Any]) -> None:
        """設定每日排程"""
        self.logger.info(f"設定每日排程，執行時間: {time_str}")
        schedule.every().day.at(time_str).do(job_func)
    
    def run_pending(self) -> None:
        """執行待處理的排程"""
        schedule.run_pending()
    
    def clear_all(self) -> None:
        """清除所有排程"""
        self.logger.info("清除所有排程")
        schedule.clear()


class BackupValidator:
    """備份驗證器實作"""
    
    def __init__(self, logger: ILogger, file_ops: IFileOperations):
        self.logger = logger
        self.file_ops = file_ops
    
    def validate(self, source: Path, backup: Path) -> bool:
        """驗證備份的完整性"""
        try:
            self.logger.info("開始驗證備份完整性")
            
            if not self.file_ops.directory_exists(backup):
                self.logger.error("備份目錄不存在")
                return False
            
            source_files = self.file_ops.count_files(source)
            backup_files = self.file_ops.count_files(backup)
            
            self.logger.info(f"來源文件數: {source_files}, 備份文件數: {backup_files}")
            
            if source_files == backup_files:
                self.logger.info("備份完整性驗證通過")
                return True
            else:
                self.logger.error("備份完整性驗證失敗：文件數量不匹配")
                return False
                
        except Exception as e:
            self.logger.error(f"驗證備份時發生錯誤: {e}")
            return False


class AutomatedBackupService:
    """自動化備份服務實作"""
    
    def __init__(
        self,
        config: BackupConfiguration,
        logger: ILogger,
        file_ops: IFileOperations,
        scheduler: IScheduler,
        validator: IBackupValidator
    ):
        self.config = config
        self.logger = logger
        self.file_ops = file_ops
        self.scheduler = scheduler
        self.validator = validator
        
        # 配置已經在 __post_init__ 中轉換為 Path 物件
        self.source_dir = config.source_dir
        self.destination_dir = config.destination_dir
        
        # 確保目標目錄存在
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"初始化備份服務 - 來源: {self.source_dir}, 目標: {self.destination_dir}")
    
    def backup(self) -> BackupResult:
        """執行備份"""
        today = datetime.date.today()
        dest_dir = self.destination_dir / str(today)
        
        self.logger.info(f"開始備份程序 - 目標路徑: {dest_dir}")
        
        # 檢查來源目錄是否存在
        if not self.file_ops.directory_exists(self.source_dir):
            error_msg = f"來源目錄不存在: {self.source_dir}"
            self.logger.error(error_msg)
            return BackupResult(
                success=False,
                message=error_msg,
                source_path=self.source_dir
            )
        
        # 如果目標目錄已存在，先刪除
        if self.file_ops.directory_exists(dest_dir):
            self.logger.warning(f"目標目錄已存在，將覆蓋: {dest_dir}")
            if not self.file_ops.delete_directory(dest_dir):
                error_msg = "刪除現有目錄失敗"
                return BackupResult(
                    success=False,
                    message=error_msg,
                    source_path=self.source_dir,
                    destination_path=dest_dir
                )
        
        # 獲取來源目錄資訊
        total_size = self.file_ops.get_directory_size(self.source_dir)
        file_count = self.file_ops.count_files(self.source_dir)
        
        # 執行備份
        start_time = time.time()
        success = self.file_ops.copy_directory(self.source_dir, dest_dir)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if not success:
            error_msg = "備份複製失敗"
            return BackupResult(
                success=False,
                message=error_msg,
                source_path=self.source_dir,
                destination_path=dest_dir,
                duration=duration
            )
        
        self.logger.info(f"備份完成! 耗時: {duration:.2f} 秒")
        
        # 驗證備份完整性（如果啟用）
        validation_success = True
        if self.config.enable_validation:
            validation_success = self.validator.validate(self.source_dir, dest_dir)
        
        result_message = "備份成功完成"
        if not validation_success:
            result_message += "，但驗證失敗"
        
        return BackupResult(
            success=success and validation_success,
            message=result_message,
            source_path=self.source_dir,
            destination_path=dest_dir,
            duration=duration,
            file_count=file_count,
            total_size=total_size
        )
    
    def setup_schedule(self, time_str: Optional[str] = None) -> None:
        """設定定時備份"""
        schedule_time = time_str or self.config.schedule_time
        self.scheduler.schedule_daily(schedule_time, self.backup)
    
    def run_scheduler(self) -> None:
        """運行排程器"""
        self.logger.info("排程器開始運行... (按 Ctrl+C 結束)")
        
        try:
            while True:
                self.scheduler.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("收到中斷信號，正在停止排程器...")
        except Exception as e:
            self.logger.error(f"排程器運行時發生錯誤: {e}")
        finally:
            self.logger.info("排程器已停止")
    
    def __enter__(self):
        """Context manager 進入"""
        self.logger.info("進入備份服務 context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 退出"""
        if exc_type:
            self.logger.error(f"Context 中發生異常: {exc_val}")
        self.scheduler.clear_all()
        self.logger.info("退出備份服務 context")


# ===== 依賴注入容器 =====
class DIContainer:
    """簡單的依賴注入容器"""
    
    def __init__(self):
        self._services: Dict[type, Callable[[], Any]] = {}
        self._singletons: Dict[type, Any] = {}
    
    def register_singleton(self, interface: type, implementation: Any) -> None:
        """註冊單例服務"""
        self._singletons[interface] = implementation
    
    def register_transient(self, interface: type, factory: Callable[[], Any]) -> None:
        """註冊瞬態服務"""
        self._services[interface] = factory
    
    def get_service(self, interface: type) -> Any:
        """獲取服務實例"""
        if interface in self._singletons:
            return self._singletons[interface]
        
        if interface in self._services:
            return self._services[interface]()
        
        raise ValueError(f"Service {interface} not registered")


def configure_services(config: BackupConfiguration) -> DIContainer:
    """配置服務容器"""
    container = DIContainer()
    
    # 註冊日誌服務 (單例)
    log_dir = Path(__file__).parent / 'logs'
    logger = FileLogger(
        str(log_dir),
        config.max_log_size,
        config.log_backup_count
    )
    container.register_singleton(ILogger, logger)
    
    # 註冊文件操作服務 (單例)
    file_ops = FileOperations(logger)
    container.register_singleton(IFileOperations, file_ops)
    
    # 註冊排程器服務 (單例)
    scheduler = ScheduleWrapper(logger)
    container.register_singleton(IScheduler, scheduler)
    
    # 註冊驗證器服務 (單例)
    validator = BackupValidator(logger, file_ops)
    container.register_singleton(IBackupValidator, validator)
    
    # 註冊備份服務 (瞬態)
    container.register_transient(
        IBackupService,
        lambda: AutomatedBackupService(
            config,
            container.get_service(ILogger),
            container.get_service(IFileOperations),
            container.get_service(IScheduler),
            container.get_service(IBackupValidator)
        )
    )
    
    return container


def main():
    """主函數"""
    # 建立配置
    config = BackupConfiguration(
        source_dir="/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/FromBeginnerToAdvanced",
        destination_dir="/home/carlos_nnb_ubuntu/projects/PythonProjectsFromBeginnerToAdvancedNotes/Backups",
        schedule_time="18:57",
        enable_validation=True
    )
    
    # 設定依賴注入容器
    container = configure_services(config)
    
    # 使用 context manager 管理備份服務
    with container.get_service(IBackupService) as backup_service:
        logger = container.get_service(ILogger)
        
        # 立即執行一次備份來測試功能
        print("開始執行備份測試...")
        result = backup_service.backup()
        
        if result.success:
            print("✓ 備份測試成功完成")
            logger.info(f"備份結果: {result.message}")
            if result.duration:
                logger.info(f"耗時: {result.duration:.2f} 秒")
            if result.file_count:
                logger.info(f"文件數量: {result.file_count}")
        else:
            print("✗ 備份測試失敗")
            logger.error(f"備份失敗: {result.message}")
            return
        
        # 設定定時備份
        backup_service.setup_schedule()
        
        # 運行排程器
        backup_service.run_scheduler()


if __name__ == "__main__":
    main()
