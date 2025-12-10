from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, Path, Depends, status
from pydantic import BaseModel, Field

# 1. 建立 FastAPI 實例
app = FastAPI(
    title="新手入門教學 API",
    description="這是一個示範 FastAPI 核心功能的範例",
    version="1.0.0"
)

# --- 模擬資料庫 (用 List 代替真實 DB) ---
fake_db = []

# --- Pydantic 模型 (定義資料長什麼樣子) ---
# 這解決了「資料驗證」的問題
class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="筆記型電腦")
    price: float = Field(..., gt=0, description="價格必須大於 0", example=25000.0)
    is_offer: Optional[bool] = Field(default=None, description="是否特價中")

class ItemResponse(Item):
    id: int

# --- 依賴注入 (Dependency) ---
# 這解決了「共用邏輯」的問題，例如分頁功能
def common_pagination(
    skip: int = Query(0, ge=0, description="跳過幾筆"),
    limit: int = Query(10, le=100, description="限制回傳筆數")
):
    return {"skip": skip, "limit": limit}

# ================= API 路徑 (Endpoints) =================

# 1. GET: 讀取資料 (使用 Query Parameters)
# 網址範例: /items/?skip=0&limit=5
@app.get("/items/", response_model=List[ItemResponse])
def read_items(pagination: dict = Depends(common_pagination)):
    """
    取得所有商品列表 (支援分頁)
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    # 模擬從資料庫切片取資料
    return fake_db[skip : skip + limit]

# 2. GET: 讀取單一資料 (使用 Path Parameters)
# 網址範例: /items/1
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(
    item_id: int = Path(..., title="商品 ID", ge=1) # 驗證 ID 必須大於等於 1
):
    """
    根據 ID 取得特定商品
    """
    # 搜尋模擬資料庫
    for item in fake_db:
        if item["id"] == item_id:
            return item
    
    # 解決「錯誤處理」問題
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="找不到該商品"
    )

# 3. POST: 新增資料 (使用 Body)
@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    """
    新增一個商品
    FastAPI 會自動驗證傳入的 JSON 是否符合 Item 模型的定義
    """
    # 模擬產生 ID
    new_id = len(fake_db) + 1
    # 將 Pydantic 模型轉為 dict 並加上 ID
    item_dict = item.model_dump() 
    item_dict["id"] = new_id
    
    fake_db.append(item_dict)
    return item_dict

# 4. PUT: 更新資料
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    """
    更新商品資訊
    """
    for index, db_item in enumerate(fake_db):
        if db_item["id"] == item_id:
            updated_data = item.model_dump()
            updated_data["id"] = item_id
            fake_db[index] = updated_data
            return updated_data
            
    raise HTTPException(status_code=404, detail="找不到要更新的商品")

# 5. 測試用 Hello World
@app.get("/")
def root():
    return {"message": "歡迎來到 FastAPI 教學！請前往 /docs 查看自動生成的文件"}

# uvicorn main_20251209_v2_old:app --reload