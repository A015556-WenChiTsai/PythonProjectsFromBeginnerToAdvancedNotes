import uvicorn
from fastapi import FastAPI, APIRouter

# ==========================================
# 模擬檔案 A: users.py (處理使用者相關邏輯)
# ==========================================
# 我們不直接用 app，而是創建一個 "路由器"
router_users = APIRouter(prefix="/users", tags=["使用者區"])

@router_users.get("/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router_users.get("/me")
def read_user_me():
    return {"username": "Current User"}


# ==========================================
# 模擬檔案 B: items.py (處理商品相關邏輯)
# ==========================================
# 這裡定義另一個路由器
router_items = APIRouter(prefix="/items", tags=["商品區"])

@router_items.get("/")
def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]

@router_items.get("/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id, "name": "The Great Gadget"}


# ==========================================
# 模擬檔案 C: main.py (主程式入口)
# ==========================================
# 這是整個應用程式的「總指揮」
app = FastAPI(title="我的大型專案架構範例")

# 【關鍵步驟】：將上面定義好的路由器 (Router) 掛載進來
# 就像把分類好的資料夾放進檔案櫃一樣
app.include_router(router_users)
app.include_router(router_items)

@app.get("/")
def root():
    return {"message": "歡迎來到主頁，請查看 /docs 以測試不同模組的 API"}


# ==========================================
# 啟動區 (讓你可以直接執行此檔案)
# ==========================================
if __name__ == "__main__":
    # 這裡使用了 uvicorn 來啟動服務
    # 執行後，請打開瀏覽器訪問 http://127.0.0.1:8000/docs
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    print("啟動服務中... 請打開瀏覽器訪問 http://127.0.0.1:8000/docs")
    uvicorn.run("modular_app_demo:app", host="127.0.0.1", port=8000, reload=True)