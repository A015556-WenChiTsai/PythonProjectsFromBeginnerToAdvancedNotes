from typing import Annotated, Any
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Form, File, UploadFile, HTTPException, status
from pydantic import BaseModel, Field

# 建立 FastAPI 實例
app = FastAPI(
    title="新手入門教學 API (Pythonic 版)",
    description="使用 Python 3.10+ 新語法與最佳實踐",
    version="2.0.0"
)

# --- Pydantic 模型 (Models) ---

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    # Pythonic 改變 1: 使用 ... 代表必填欄位，語意更清晰
    name: str = Field(..., example="iPhone 15", description="商品名稱")
    
    # Pythonic 改變 2: 使用 `str | None` 代替 `Union[str, None]` (Python 3.10+)
    description: str | None = Field(default=None, description="商品描述")
    
    price: float = Field(gt=0, description="價格必須大於 0")
    
    # Pythonic 改變 3: 對於 List/Dict 等可變物件，建議使用 default_factory
    # 這樣可以避免所有實例共用同一個 list 的潛在問題
    tags: list[str] = Field(default_factory=list)
    
    image: Image | None = None

class UserBase(BaseModel):
    username: str
    email: str

class UserOut(UserBase):
    """ 輸出的模型，不包含密碼 """
    pass

class UserIn(UserBase):
    """ 輸入的模型，包含密碼 """
    password: str

# --- API 路徑操作 (Path Operations) ---

@app.get("/", tags=["基礎"])
async def root() -> dict[str, str]:
    """ 最簡單的 Hello World，加上回傳型別提示 """
    return {"message": "Hello World"}

@app.get("/items/{item_id}", tags=["查詢"])
async def read_item(
    # Pythonic 改變 4: 統一使用 Annotated，這是 FastAPI 推薦的現代寫法
    # 讓型別定義與驗證邏輯分離，閱讀性更高
    item_id: Annotated[int, Path(title="商品 ID", ge=1)], 
    q: Annotated[str | None, Query(max_length=50)] = None,
    short: bool = False
) -> dict[str, Any]:
    
    item = {"item_id": item_id}
    if q:
        item["q"] = q
    if not short:
        item["description"] = "這是一個詳細的商品描述..."
    return item

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["新增"])
async def create_item(item: Item) -> Item:
    """ 
    接收 JSON Body
    回傳型別標註為 -> Item，讓 IDE 能提供更好的自動補全
    """
    return item

@app.post("/users/", response_model=UserOut, tags=["使用者"])
async def create_user(user: UserIn) -> UserIn:
    """ Response Model 會自動過濾掉 UserIn 中的 password """
    return user

@app.get("/info/", tags=["進階參數"])
async def read_info(
    # 使用 | None 讓程式碼更短更乾淨
    user_agent: Annotated[str | None, Header()] = None,
    ads_id: Annotated[str | None, Cookie()] = None
) -> dict[str, str | None]:
    return {"User-Agent": user_agent, "ads_id": ads_id}

@app.post("/login/", tags=["表單與檔案"])
async def login(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()]
) -> dict[str, str]:
    return {"username": username}

@app.post("/uploadfile/", tags=["表單與檔案"])
async def create_upload_file(
    file: Annotated[UploadFile, File(description="請上傳一個檔案")]
) -> dict[str, str | None]:
    if not file:
        return {"message": "No file sent"}
    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/items-check/{item_id}", tags=["錯誤處理"])
async def read_item_check(item_id: int) -> dict[str, int]:
    if item_id == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # 使用常數而非數字 404，更具可讀性
            detail="Item not found",
            headers={"X-Error": "Error 0"},
        )
    return {"item_id": item_id}

# --- Pythonic 改變 5: 程式入口點 ---
# 這讓你可以直接用 `python main_20251209.py` 執行，
# 也可以用 `uvicorn main_20251209:app` 執行，更有彈性。

if __name__ == "__main__":
    import uvicorn
    # 這裡設定 host="0.0.0.0" 讓區域網路內的其他電腦也能訪問
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    uvicorn.run("fastapi_cheatsheet:app", host="127.0.0.1", port=8000, reload=True)