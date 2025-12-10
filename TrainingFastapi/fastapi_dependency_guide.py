import uvicorn
import logging
from dataclasses import dataclass
from typing import Annotated, Iterator, Any
from fastapi import FastAPI, Depends, Header, HTTPException, Request, status

# 設定標準 Logging (比 print 更 Pythonic，生產環境標準)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# ==============================================================================
# 1. [Global Dependencies] 全域依賴
# Pythonic 點評：使用 async 定義 I/O 相關操作，並使用 logging 取代 print
# ==============================================================================

async def log_transaction(request: Request):
    """全域依賴：紀錄請求路徑"""
    logger.info(f"[Global] 收到請求 -> {request.method} {request.url.path}")

# 註冊全域依賴
app.router.dependencies.append(Depends(log_transaction))


# ==============================================================================
# 2. [Dependencies with yield] 帶有 yield 的依賴
# Pythonic 點評：使用 Iterator 型別提示，比 Generator 更簡潔通用
# ==============================================================================

def get_db_session() -> Iterator[str]:
    """
    模擬資料庫連線 (Context Manager Pattern)
    """
    db_connection = "DB_Session_#123"
    logger.info("[Dependency] DB 連線開啟 (Setup)")
    
    try:
        yield db_connection
    finally:
        logger.info("[Dependency] DB 連線關閉 (Teardown)")


# ==============================================================================
# 3. [Classes as Dependencies] 類別作為依賴
# Pythonic 點評：使用 @dataclass！
# 這比傳統 class 寫法少寫很多 boilerplate code (如 __init__)
# ==============================================================================

@dataclass
class PaginationParams:
    """
    使用 @dataclass 自動生成 __init__，程式碼極度簡潔。
    FastAPI 完美支援 dataclass 作為依賴。
    """
    q: str | None = None
    skip: int = 0
    limit: int = 100

    @property
    def is_filtered(self) -> bool:
        return self.q is not None


# ==============================================================================
# 4. [Sub-dependencies] 子依賴
# Pythonic 點評：Annotated 是現代 Python (3.9+) 的標準寫法
# ==============================================================================

def extract_token(x_token: Annotated[str, Header()]) -> str:
    if x_token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="X-Token header invalid"
        )
    return x_token

# 這裡展示依賴鏈：get_current_user -> extract_token
def get_current_user(token: Annotated[str, Depends(extract_token)]) -> dict[str, Any]:
    logger.info("[Sub-Dependency] Token 驗證通過，查找使用者...")
    return {"id": 1, "username": "python_master", "role": "admin"}


# ==============================================================================
# 5. [Dependencies in Decorators] 裝飾器中的依賴
# ==============================================================================

def require_admin(user: Annotated[dict, Depends(get_current_user)]):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="權限不足")
    logger.info("[Decorator] Admin 權限確認")


# ==============================================================================
# 路由實作
# ==============================================================================

@app.get("/items/")
def read_items(
    # @dataclass 讓這裡看起來非常優雅
    params: Annotated[PaginationParams, Depends()],
    db: Annotated[str, Depends(get_db_session)]
):
    logger.info(f"[Path Operation] 處理業務邏輯，使用 DB: {db}")
    return {
        "data": ["item_A", "item_B"],
        "params": params,  # dataclass 可以直接被序列化
        "filtered": params.is_filtered
    }

@app.get("/admin/", dependencies=[Depends(require_admin)])
def admin_dashboard():
    return {"message": "歡迎來到管理員後台"}

# ==============================================================================
# 啟動點
# ==============================================================================
if __name__ == "__main__":
    print("\n--- 服務啟動中 (請使用 Postman 測試) ---")
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    print("1. 一般查詢: http://127.0.0.1:8000/items/?q=test&limit=5")
    print("2. 管理員區: http://127.0.0.1:8000/admin/ (需 Header 'X-Token: secret-token')\n")
    uvicorn.run("fastapi_dependency_guide:app", host="127.0.0.1", port=8000, reload=True)