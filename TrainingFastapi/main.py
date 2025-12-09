from enum import Enum
from typing import Union
from typing import Annotated, Literal
from fastapi import FastAPI, Query, Path, Body,Cookie,Header
from pydantic import BaseModel, Field,HttpUrl  # <--- 重點：一定要引入這個
from datetime import datetime, time, timedelta
from uuid import UUID
from decimal import Decimal
app = FastAPI()

# ❌ 舊寫法：參數列超級長，很難維護
@app.get("/items/")
async def read_items(
    session_id: str = Cookie(),
    user_id: str = Cookie(),
    tracking_id: str | None = Cookie(default=None),
    theme: str = Cookie(),
    language: str = Cookie(),
):
    return {"session": session_id, "user": user_id}


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None  # 這是選填的，沒有也沒關係

# 步驟 2: 在路徑操作中使用這個模型
@app.get("/items2/")
async def read_items2(
    # 重點在這裡！
    # 我們告訴 FastAPI：請把讀取到的 Cookie，依照 Cookies 類別的規則，裝進去
    cookies: Annotated[Cookies, Cookie()]
):
    # 現在，你可以用 . 屬性來存取，編輯器還會有自動補全！
    return {
        "session_id": cookies.session_id,
        "fatebook_tracker": cookies.fatebook_tracker
    }
# Cookie Parameter Models
# Cookie 參數模型

# # Header Parameters
# # 頭部參數 
# @app.get("/items/")
# # 這裡的意思是：請去讀取一個叫做 "user-agent" 的 Header，並把它放進 user_agent 這個變數
# async def read_items(user_agent: Annotated[str | None, Header()] = None):
#     return {"User-Agent": user_agent}


# @app.get("/items2/")
# # Python 變數叫 strange_header
# # FastAPI 會自動去抓 HTTP Header 裡的 "strange-header"
# async def read_items2(strange_header: Annotated[str | None, Header()] = None):
#     return {"strange_header": strange_header}

# @app.get("/items3/")
# # 注意這裡型別是 list[str]
# async def read_items3(x_token: Annotated[list[str] | None, Header()] = None):
#     return {"X-Token values": x_token}

# # Cookie Parameters
# # Cookie 參數
# # 用power Shell執行
# # curl.exe -X GET "http://127.0.0.1:8000/items/" -H "accept: application/json" -H "Cookie: ads_id=111"
# # 就正常了
# @app.get("/items/")
# async def read_items(
#     # 2. 定義參數
#     # ads_id: 變數名稱 (對應到瀏覽器傳來的 cookie 名稱)
#     # str | None: 型別，可能是字串，也可能是 None (如果沒傳 cookie)
#     # Cookie(default=None): 告訴 FastAPI 去讀取 Cookie，如果沒讀到，預設值為 None
#     ads_id: Annotated[str | None, Cookie()] = None
# ):
#     return {"ads_id": ads_id}

# # Extra Data Types
# # 額外資料類型 
# # 模擬一個處理維護紀錄的 API
# # PUT /maintenance/{log_id}
# @app.put("/maintenance/{log_id}")
# async def update_maintenance_log(
#     log_id: UUID,                 # 1. 自動驗證並轉換為 UUID 物件
#     start_time: datetime = Body(), # 2. 自動讀取 JSON 中的時間字串，轉為 datetime
#     duration: timedelta = Body(),  # 3. 自動讀取總秒數，轉為 timedelta (時間長度)
#     cost: Decimal = Body()         # 4. 自動讀取數字，轉為高精度的 Decimal (適合金錢)
# ):
#     # --- 這裡是 Python 邏輯區 ---
#     # 在這裡，變數已經是 Python 的物件了，不是純字串！
    
#     # 範例：計算結束時間 (時間物件可以直接相加，超方便)
#     end_time = start_time + duration
    
#     # 範例：計算含稅成本 (Decimal 計算不會有誤差)
#     total_cost = cost * Decimal("1.05") 

#     return {
#         "message": "Log updated successfully",
#         "log_id": log_id,             # FastAPI 會自動把它轉回字串傳給前端
#         "start_time": start_time,     # FastAPI 會自動轉回 ISO 格式字串
#         "end_time": end_time,
#         "total_cost": total_cost
#     }


# # Declare Request Example Data
# # 聲明請求範例資料
# class Item(BaseModel):
#     # 重點在這裡：使用 Field(examples=[...])
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice Item"])
#     price: float = Field(examples=[35.4])
#     tax: float | None = Field(default=None, examples=[3.2])

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

#     # 重點在這裡：定義一個 model_config
#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 }
#             ]
#         }
#     }

# @app.put("/items2/{item_id}")
# async def update_item2(item_id: int, item: Item):
#     return {"item_id": item_id, "item": item}

# # 這裡定義了多個範例
# @app.put("/items3/{item_id}")
# async def update_item3(
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             openapi_examples={
#                 "正常範例": {
#                     "summary": "一個正常的商品",
#                     "description": "這是標準的範例資料。",
#                     "value": {
#                         "name": "Foo",
#                         "price": 35.4,
#                         "tax": 3.2,
#                     },
#                 },
#                 "無效稅率範例": {
#                     "summary": "免稅商品",
#                     "description": "這是一個沒有稅金的商品範例。",
#                     "value": {
#                         "name": "Bar",
#                         "price": 19.9,
#                         "tax": 0,
#                     },
#                 },
#             }
#         ),
#     ],
# ):
#     return {"item_id": item_id, "item": item}

# # Body - Nested Models
# # 正文 - 嵌套模型
# # 1. 先定義一個比較小的模型：圖片 (Image)
# class Image(BaseModel):
#     url: HttpUrl          # 這裡會強制檢查是否為網址格式
#     name: str

# # 2. 再定義主要的模型：商品 (Item)
# class Item(BaseModel):
#     name: str=Field(..., title="商品名稱",min_length=1, max_length=2)
#     description: str | None = None
#     price: float
#     tags: set[str] = set()  # 重點一：使用 Set 來自動去重複
    
#     # 重點二 & 三：這裡引用了上面的 Image 模型
#     # 這代表 image 欄位必須符合 Image 類別的結構
#     # list[Image] 代表這裡可以放「好幾張」圖片
#     images: list[Image] | None = None 

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     # 當程式跑到這裡時，FastAPI 已經幫你把 JSON 轉成 Python 物件了
#     # 而且內層的 images 也都驗證過了
#     results = {"item_id": item_id, "item": item}
#     return results

# # Body - Fields
# # 主體 - 字段
# # 定義我們的資料模型
# class Item(BaseModel):
#     # 重點 2: name 是必填的，且我們加上了驗證規則
#     # ... (Ellipsis) 代表這個欄位是「必填 (Required)」
#     # title 會顯示在 API 文件上
#     # max_length=300 代表如果前端傳超過 300 字，API 會直接報錯
#     name: str = Field(..., title="商品名稱",min_length=1, max_length=2)

#     # 重點 3: description 是選填的 (可以是 None)
#     # 我們加上了 description，讓看文件的人知道這是幹嘛的
#     description: Union[str, None] = Field(
#         default=None, 
#         title="商品描述", 
#         description="這裡可以寫很長的商品介紹"
#     )

#     # 重點 4: price 是必填的數值，且必須大於 0
#     # gt = Greater Than (大於)
#     price: float = Field(..., gt=0, description="價格必須大於 0")

#     # 重點 5: tax 是選填的
#     tax: Union[float, None] = None

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     # 當程式跑到這裡時，FastAPI 已經幫你確認過：
#     # 1. name 長度沒爆
#     # 2. price 確實大於 0
#     # 你可以放心處理邏輯
#     results = {"item_id": item_id, "item": item}
#     return results

# # Body - Multiple Parameters
# # 正文 - 多個參數
# class Item(BaseModel):
#     name: str
#     price: float


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int = Path(..., title="商品的 ID"),  # 1. Path 參數 (來自網址路徑)
#     q: str | None = None,  # 2. Query 參數 (來自網址 ?q=xxx)
#     item: Item = None,  # 3. Body 參數 (來自請求的 JSON 內容)
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results


# class Item(BaseModel):
#     name: str
#     description: str | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None


# @app.put("/items2/{item_id}")
# async def update_item2(item_id: int, item: Item, user: User):  # Body 1  # Body 2
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results


# @app.put("/items3/{item_id}")
# async def update_item3(
#     item_id: int,
#     item: Item,
#     user: User,
#     importance: int = Body(...),  # 這裡用了 Body，強制它成為 JSON 的一部分
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     return results


# # 無 embed=True
# class Item(BaseModel):
#     name: str
#     price: float


# @app.post("/items4/")
# async def create_item4(item: Item):
#     return item


# # {
# #   "name": "aaa",
# #   "price": 111
# # }
# @app.put("/items4/{item_id}")
# async def update_item4(
#     item_id: int, item: Item = Body(..., embed=True)  # 加上 embed=True
# ):
#     return {"item_id": item_id, "item": item}


# {
#   "item_id": 2,
#   "item": {
#     "name": "bbbb",
#     "price": 333
#   }
# }

# # 查詢參數模型
# # 參數太多，函式定義變得很長，很難閱讀
# @app.get("/items/")
# async def read_items(
#     q: str | None = None,
#     page: int = 1,
#     size: int = 10,
#     sort: str = "date",
#     category: str | None = None
# ):
#     return {"q": q, "page": page} # ...略

# # 這裡定義了一個模型，叫做 FilterParams
# # 你可以把它想像成一個「過濾器設定檔」
# class FilterParams(BaseModel):
#     # model_config 是 Pydantic 的設定，這裡設為 forbid 代表「不允許傳入未定義的參數」
#     model_config = {"extra": "forbid"}

#     # 定義每頁筆數，預設 100，必須大於 0 (gt=0)，小於等於 100 (le=100)
#     limit: int = Field(100, gt=0, le=100)

#     # 定義偏移量（從第幾筆開始），預設 0，必須大於等於 0
#     offset: int = Field(0, ge=0)

#     # 定義排序欄位，預設是 created_at，且只能選 "created_at" 或 "updated_at"
#     order_by: Literal["created_at", "updated_at"] = "created_at"

#     # 定義標籤，這是一個列表，預設是空列表
#     tags: list[str] = []

# @app.get("/items2/")
# # 重點在這裡！
# # 我們告訴 FastAPI：請把網址上的查詢參數，依照 FilterParams 的規則抓下來
# async def read_items2(filter_query: Annotated[FilterParams, Query()]):
#     # 這裡的 filter_query 已經是一個物件了，可以直接用 . 來存取
#     return {
#         "limit": filter_query.limit,
#         "offset": filter_query.offset,
#         "order_by": filter_query.order_by,
#         "tags": filter_query.tags
#     }

# Path Parameters and Numeric Validations¶
# 路徑參數和數值驗證
# @app.get("/books/{book_id}")
# def get_book(
#     # 重點在這裡！
#     # 我們宣告 book_id 是整數，並使用 Path 來設定規則
#     book_id: int = Path(
#         title="書籍 ID",    # 在自動文件中顯示的標題
#         ge=1,              # greater than or equal to 1 (大於等於 1)
#         le=1000            # less than or equal to 1000 (小於等於 1000)
#     ),
#     q: str | None = None   # 這是一個額外的查詢參數 (選填)
# ):
# 如果使用者傳入 /books/500 -> 成功
# 如果使用者傳入 /books/0   -> 失敗 (FastAPI 會自動報錯)
# 如果使用者傳入 /books/1001 -> 失敗
# return {"book_id": book_id, "query": q}
# Query Parameters and String Validations¶
# 查詢參數和字串驗證
# @app.get("/items/")
# async def read_items(
#     # 翻譯：q 是一個字串，預設是 None (可選的)，但如果有值，長度必須在 3 到 50 之間
#     q: Annotated[str | None, Query(min_length=3, max_length=4)] = None
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items2/")
# async def read_items2(
#     # 翻譯：q 必須符合這個正規表達式規則 (例如只能是固定字串或特定格式)
#     q: Annotated[str | None, Query(pattern="^fixedquery$")] = None
# ):
#     # ... 略
#     return {"q": q}

# @app.get("/items3/")
# async def read_items3(
#     # 翻譯：q 必須符合這個正規表達式規則 (例如只能是固定字串或特定格式)
#     q: Annotated[str, Query(min_length=3)] = ...
# ):
#     # ... 略
#     return {"q": q}

# @app.get("/items4/")
# async def read_items4(
#     # 翻譯：q 是一個字串列表 (List[str])
#     # q: Annotated[list[str] | None, Query()] = None
#     q: Annotated[list[str] | None, Query(min_length=1)] = None
# ):
#     return {"q": q}

# @app.get("/items5/")
# async def read_items5(
#     q: Annotated[str | None, Query(
#         title="搜尋關鍵字",
#         description="請輸入您想搜尋的產品名稱，支援模糊搜尋",
#         alias="item-query", # 允許網址用 ?item-query=... 來傳參數
#         deprecated=True # 標記這個參數快被淘汰了，文件上會顯示警告
#     )] = None
# ):
#     return {"q": q}
#############################
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


# @app.get("/items2/{item_id}")
# async def read_item2(item_id: int):
#     return {"item_id": item_id}


# @app.get("/users")
# async def read_users():
#     return ["Rick", "Morty"]


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# async def read_item3(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items4/{item_id}")
# async def read_item4(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


# @app.get("/items5/{item_id}")
# async def read_user_item(
#     item_id: str,      # 這是「路徑參數」，因為它出現在上面的 URL {} 裡
#     needy: str,        # 這是「必選查詢參數」，因為它沒有預設值 (= ...)
#     skip: int = 0,     # 這是「選填查詢參數」，因為它有預設值 = 0
#     limit: int | None = None # 這是「選填查詢參數」，預設是 None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item

# # 1. 定義你的資料模型 (這就是那張「申請表」的藍圖)
# # 繼承 BaseModel 是規矩，照做就對了
# class Item(BaseModel):
#     name: str = Field(min_length=1, title="商品名稱")          # 必填，必須是字串
#     description: str | None = None  # 選填，預設是 None (沒填也沒關係)
#     price: float             # 必填，必須是數字 (有小數點)
#     tax: float = 10.5        # 選填，如果沒填，稅金預設就是 10.5

# # 2. 建立 API 路徑
# # 這裡用 POST，因為我們要「新增」資料
# @app.post("/items/")
# async def create_item(item: Item): # <--- 重點：把參數型別設為上面定義的 Item

#     # 到了這裡，item 已經是一個被驗證過、乾淨的 Python 物件了
#     # 你可以直接用 item.name 或 item.price 來取值

#     # 這裡我們做個簡單的運算：計算含稅價格
#     total_price = item.price + item.tax

#     # 回傳結果給前端
#     return {"item_name": item.name, "total_price": total_price}
