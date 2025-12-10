from typing import Annotated, List, Optional

from fastapi import FastAPI, HTTPException, Query, Path, Depends, status
from pydantic import BaseModel, Field

# --- 1. 初始化 App (改進點：將全域筆記放入 description) ---
# 這裡的 description 支援 Markdown，適合放整體的架構說明
app_description = """
這是一個教學用的 FastAPI 範例，展示了最佳實踐與現代化語法。

### 📚 學習重點 (架構面)
1. **模擬資料庫 (Dict)**: 
    - 使用 `Dict[int, dict]` 取代 List。
    - 優點：查詢速度為 O(1)，比 List 的 O(n) 更快，且程式碼更簡潔。
2. **Pydantic 模型**: 
    - 採用繼承 (`ItemBase`) 與分離 (`Create`/`Response`) 策略。
    - 符合 DRY (Don't Repeat Yourself) 原則。
3. **依賴注入 (Dependency Injection)**:
    - 將分頁邏輯封裝在 `PaginationParams` 類別中，讓路徑函式更乾淨。
"""

app = FastAPI(
    title="Pythonic FastAPI 開發工具書",
    description=app_description,
    version="2.1.0",
    contact={
        "name": "你的名字",
        "email": "your@email.com",
    },
)

# --- 模擬資料庫 ---
fake_db: dict[int, dict] = {}

# --- Pydantic 模型 ---


class ItemBase(BaseModel):
    """
    **基礎模型 (Base Model)**

    包含所有模型共用的欄位。
    - 設定了 `min_length`, `max_length` 等驗證條件。
    
    ...:在 Pydantic 裡，它代表 「必填 (Required)
    min_length=2: 限制最短長度為 2
    max_length=50: 限制最長長度為 50
    gt=0: Greater Than (大於)，價格必須大於 0
    gt (Greater Than): > (大於)
    ge (Greater than or Equal): >= (大於等於)
    如果你允許商品價格是 0 元（例如免費贈品），就要改用 ge=0。
    lt (Less Than): < (小於)
    le (Less than or Equal): <= (小於等於)
    """

    name: str = Field(
        ..., min_length=2, max_length=50, example="機械式鍵盤", description="商品名稱"
    )
    price: float = Field(..., gt=0, description="價格必須大於 0", example=3500.0)
    is_offer: bool = Field(default=False, description="是否特價中")


class ItemCreate(ItemBase):
    """
    **建立用模型 (Create Model)**

    繼承自 `ItemBase`。
    - 使用者建立商品時**不需要**傳入 `id`，所以這裡不包含 id 欄位。
    """

    pass


class ItemResponse(ItemBase):
    """
    **回傳用模型 (Response Model)**

    繼承自 `ItemBase`。
    - 回傳給前端時，必須包含資料庫產生的 `id`。
    - 這樣做符合 DRY 原則，不用重複寫 name, price...
    """

    id: int


# --- 依賴注入 ---


class PaginationParams:
    """
    **分頁參數依賴**

    將 `skip` 和 `limit` 的邏輯封裝在這裡，
    任何需要分頁的 API 都可以直接注入此類別。
    """

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="跳過幾筆 (Offset)"),
        limit: int = Query(10, le=100, description="限制回傳筆數 (Limit)"),
    ):
        self.skip = skip
        self.limit = limit


# 使用 Annotated 簡化型別宣告
PaginationDep = Annotated[PaginationParams, Depends()]

# 未簡化（傳統寫法 / Old School）
# 傳統寫法：在參數預設值裡寫 Depends
@app.get("/items_old_1/")
def read_items_old_1(
    # 這裡必須寫兩次 PaginationParams (一次是型別，一次是邏輯)
    pagination: PaginationParams = Depends(PaginationParams)
):
    return ...
# 或者稍微簡化一點點（FastAPI 聰明到可以省略括號裡的內容，但還是要寫 Depends()）：
@app.get("/items_old_2/")
def read_items_old_2(
    # 還是要在後面掛一個尾巴 = Depends()
    pagination: PaginationParams = Depends() 
):
    return ...

# ❌ 新手寫法 (重複且危險)：
# def read_items(skip: int = 0, limit: int = 10): # 這裡沒檢查 limit 上限！
# ================= API 路徑 (Endpoints) =================


@app.get(
    "/items/",
    response_model=List[ItemResponse],
    summary="取得所有商品 (List)",
    tags=["Items"],
)
def read_items(pagination: PaginationDep):
    """
    取得商品列表，支援分頁功能。

    ### 💡 技術筆記 (Implementation Note)
    1. **資料轉換**: 使用 `list(fake_db.values())` 將 Dict 的 values 轉為 List。
    2. **切片操作**: 使用 Python 原生切片 `[skip : skip + limit]` 實作分頁。
    """
    all_items = list(fake_db.values())
    return all_items[pagination.skip : pagination.skip + pagination.limit]


@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="取得單一商品 (Retrieve)",
    tags=["Items"],
)
def read_item(item_id: Annotated[int, Path(title="商品 ID", ge=1)]):
    """
    根據 ID 快速查找商品。

    ### 💡 技術筆記 (Implementation Note)
    - **Pythonic 寫法**: 直接使用 Dictionary 的 `.get(key)` 方法查找。
    - 若 key 不存在會回傳 `None`，避免了使用迴圈查找的低效能。
    - 若為 `None` 則拋出 `404 HTTPException`。
    """
    item = fake_db.get(item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {item_id} 的商品",
        )
    return item


@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新增商品 (Create)",
    tags=["Items"],
)
def create_item(item_in: ItemCreate):
    """
    新增商品到資料庫。

    ### 💡 技術筆記 (Implementation Note)
    1. **ID 生成**: 簡單實作使用 `len(fake_db) + 1`。
    2. **模型轉換**: 使用 `item_in.model_dump()` 將 Pydantic 模型轉為 Python Dict。
    3. **存儲**: 將資料存入 `fake_db[new_id]`。
    """
    new_id = len(fake_db) + 1

    item_data = item_in.model_dump()
    item_data["id"] = new_id

    fake_db[new_id] = item_data

    return item_data


@app.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="更新商品 (Update)",
    tags=["Items"],
)
def update_item(item_id: Annotated[int, Path(ge=1)], item_in: ItemCreate):
    """
    更新已存在的商品資訊。

    ### 💡 技術筆記 (Implementation Note)
    - 先檢查 ID 是否存在於 `fake_db` 中，若無則拋出 404。
    - 使用 `PUT` 方法通常代表「整份替換」，這裡將新資料覆蓋舊資料。
    """
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="找不到要更新的商品"
        )

    updated_data = item_in.model_dump()
    updated_data["id"] = item_id

    fake_db[item_id] = updated_data

    return updated_data


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="刪除商品 (Delete)",
    tags=["Items"],
)
def delete_item(item_id: Annotated[int, Path(ge=1)]):
    """
    刪除指定商品。

    ### 💡 技術筆記 (Implementation Note)
    1. **Pythonic 移除**: 使用 `fake_db.pop(item_id)` 直接移除鍵值對。
    2. **HTTP 狀態碼**: 刪除成功通常回傳 `204 No Content`。
    3. **回傳值**: 204 狀態碼不需要回傳 Body，所以 `return None`。
    """
    if item_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    fake_db.pop(item_id)
    return None

if __name__ == "__main__":
    import uvicorn

    # 這裡設定 host="0.0.0.0" 讓區域網路內的其他電腦也能訪問
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    uvicorn.run("fastapi_best_practices:app", host="127.0.0.1", port=8000, reload=True)
