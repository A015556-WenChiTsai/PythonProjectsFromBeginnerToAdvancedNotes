import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

# 建立 App 實例
app = FastAPI()

# ==========================================
# 1. 定義依賴邏輯 (The Logic)
# ==========================================
def get_token_header(token: str):
    """
    這是一個模擬的依賴項函數。
    假設我們需要驗證 Token 是否為 "secret-token"。
    """
    if token != "secret-token":
        raise HTTPException(status_code=400, detail="Token 無效！")
    return f"User-With-Token-{token}"

# ==========================================
# 2. 定義 Annotated 依賴 (The Magic)
# ==========================================
# 這裡就是關鍵！我們把 str 型別和 Depends 邏輯打包成一個新名字 "RequiredToken"
# 以後只要用 RequiredToken，就自動代表：
# 1. 它是字串
# 2. 它需要執行 get_token_header 檢查
RequiredToken = Annotated[str, Depends(get_token_header)]


# ==========================================
# 3. 應用在 API 路由 (The Usage)
# ==========================================

@app.get("/items/")
def read_items(user_token: RequiredToken): 
    # 注意看上面：參數非常乾淨，沒有寫 "= Depends(...)"
    return {"message": "讀取物品成功", "user": user_token}

@app.get("/users/")
def read_users(user_token: RequiredToken):
    # 複用同一個依賴，完全不用重複寫程式碼
    return {"message": "讀取使用者列表成功", "user": user_token}

@app.get("/no-annotated/")
def old_style(token: str = Depends(get_token_header)):
    # 【對照組】這是舊寫法，比較冗長，且視覺雜亂
    return {"message": "這是舊寫法", "user": token}


# ==========================================
# 4. 啟動程式 (Entry Point)
# ==========================================
if __name__ == "__main__":
    print("🚀 伺服器啟動中...")
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    print("請打開瀏覽器測試：http://127.0.0.1:8000/items/?token=secret-token")
    print("測試失敗案例：http://127.0.0.1:8000/items/?token=wrong")
    
    # 直接執行此檔案即可啟動
    uvicorn.run("fastapi_annotated_demo:app", host="127.0.0.1", port=8000, reload=True)