import uvicorn
from fastapi import FastAPI, Depends, Header, HTTPException, Request, status
from typing import Annotated, Generator, Any

# ==============================================================================
# 1. [Global Dependencies] 全域依賴
# 概念：像是大樓的警衛，不管你去哪一樓，進大門都要先過這關。
# 用途：全域 Log、API Key 檢查、防火牆邏輯。
# ==============================================================================

async def log_transaction(request: Request):
    """
    全域依賴：紀錄每一個進來的請求方法與路徑。
    """
    print(f"\n[Global] 收到請求 -> {request.method} {request.url.path}")

# 初始化 App，並注入全域依賴
app = FastAPI(dependencies=[Depends(log_transaction)])


# ==============================================================================
# 2. [Dependencies with yield] 帶有 yield 的依賴
# 概念：像是去圖書館借書。借書(Setup) -> 看書(路徑函式執行) -> 還書(Teardown)。
# 用途：資料庫連線管理 (Session)、檔案開啟/關閉。
# ==============================================================================

def get_db_session() -> Generator[str, None, None]:
    """
    模擬資料庫連線的生命週期管理。
    """
    db_connection = "DB_Session_#123"
    print("[Dependency] 資料庫連線已開啟 (Setup)")
    
    try:
        yield db_connection  # 暫停執行，將 db 物件交給路徑函式使用
    finally:
        # 當路徑函式執行完畢後，會回來執行這裡
        print("[Dependency] 資料庫連線已關閉 (Teardown)")


# ==============================================================================
# 3. [Classes as Dependencies] 類別作為依賴
# 概念：把一堆散落在參數列的參數，打包成一個物件。
# 用途：分頁參數 (page, size)、搜尋過濾器。
# ==============================================================================

class PaginationParams:
    """
    將分頁邏輯封裝在類別中。
    FastAPI 會自動解析 Query Parameters 並填入這裡。
    """
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
        
    @property
    def is_filtered(self) -> bool:
        return self.q is not None


# ==============================================================================
# 4. [Sub-dependencies] 子依賴
# 概念：依賴可以依賴另一個依賴。像是俄羅斯娃娃。
# 用途：先解析 Token (層級1) -> 再透過 Token 查使用者 (層級2)。
# ==============================================================================

def extract_token(x_token: Annotated[str, Header()]) -> str:
    """
    (層級 1) 從 Header 提取 Token。
    """
    if x_token != "secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token 無效")
    return x_token

def get_current_user(token: Annotated[str, Depends(extract_token)]) -> dict[str, Any]:
    """
    (層級 2) 依賴 extract_token，拿到 Token 後查找使用者。
    """
    print(f"[Sub-Dependency] Token 驗證成功，正在查找使用者...")
    # 模擬資料庫查找
    return {"id": 1, "username": "new_developer", "role": "admin"}


# ==============================================================================
# 5. [Dependencies in Decorators] 裝飾器中的依賴
# 概念：我不需要這個依賴的回傳值，我只需要它幫我「把關」或「執行動作」。
# 用途：權限檢查 (Require Admin)、驗證 Header 格式。
# ==============================================================================

def require_admin_role(user: Annotated[dict, Depends(get_current_user)]):
    """
    檢查使用者是否為管理員。
    注意：這裡依賴了 get_current_user，所以會自動觸發 Token 檢查。
    """
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="權限不足")
    print("[Decorator Dependency] 管理員權限檢查通過")


# ==============================================================================
# API 路由實作 (將上述工具組合使用)
# ==============================================================================

@app.get("/items/")
def read_items(
    # 使用類別依賴：程式碼乾淨，不用寫一堆 q, skip, limit
    params: Annotated[PaginationParams, Depends(PaginationParams)],
    # 使用 Yield 依賴：自動處理 DB 開關
    db: Annotated[str, Depends(get_db_session)]
):
    """
    情境：一般查詢，需要分頁和資料庫。
    """
    print(f"[Path Operation] 正在查詢資料庫: {db}")
    return {
        "data": ["item1", "item2"],
        "pagination": params.__dict__,
        "has_filter": params.is_filtered
    }


@app.get("/users/me/")
def read_user_me(
    # 使用子依賴鏈：Header -> Token -> User
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    情境：獲取當前登入使用者資訊。
    """
    return current_user


@app.get("/admin/system_status/", dependencies=[Depends(require_admin_role)])
def read_system_status():
    """
    情境：只有管理員能看的系統狀態。
    注意：require_admin_role 放在裝飾器中，因為我們不需要它的回傳值，
    只需要它在進入函式前拋出錯誤 (如果權限不足)。
    """
    return {"status": "System All Green", "cpu_load": "15%"}


# ==============================================================================
# 程式進入點
# ==============================================================================
if __name__ == "__main__":
    print("--- FastAPI Dependency Guide 啟動中 ---")
    print("請使用 Postman 或瀏覽器測試以下情境：")
    # http://127.0.0.1:8000/docs
    print("0. [] http://127.0.0.1:8000/docs")
    print("1. [類別與Yield] http://127.0.0.1:8000/items/?q=python&limit=5")
    print("2. [子依賴]      http://127.0.0.1:8000/users/me/ (需 Header 'X-Token: secret-token')")
    print("3. [裝飾器依賴]  http://127.0.0.1:8000/admin/system_status/ (需 Header 'X-Token: secret-token')")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)