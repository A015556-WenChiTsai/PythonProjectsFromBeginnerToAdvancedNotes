from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile
import uvicorn

app = FastAPI()

# ---------------------------------------------------------
# 情境一：單純的表單資料 (Form)
# 就像你在網頁上填寫帳號密碼登入
# ---------------------------------------------------------
@app.post("/login/")
async def login(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()]
):
    # 這裡的 Form() 告訴 FastAPI：去表單資料裡找 username，不要去 JSON 裡找
    return {"message": "登入成功", "user": username}


# ---------------------------------------------------------
# 情境二：單純的檔案上傳 (File)
# 就像你在上傳大頭貼
# ---------------------------------------------------------
@app.post("/upload-file/")
async def create_upload_file(
    file: Annotated[UploadFile, File()]
):
    # UploadFile 比 bytes 更適合處理大檔案，因為它不會一次把記憶體吃光
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_info": "檔案已接收，尚未儲存"
    }


# ---------------------------------------------------------
# 情境三：表單 + 檔案同時上傳 (Form + File)
# 就像你在填寫履歷：有文字資料(名字)，也有附件(PDF)
# ---------------------------------------------------------
@app.post("/submit-profile/")
async def submit_profile(
    name: Annotated[str, Form()],
    age: Annotated[int, Form()],
    resume: Annotated[UploadFile, File()]
):
    return {
        "status": "履歷已收到",
        "applicant": name,
        "age": age,
        "resume_name": resume.filename
    }

# ---------------------------------------------------------
# 啟動點 (方便你直接執行此檔案)
# ---------------------------------------------------------
if __name__ == "__main__":
    # 執行後，請打開瀏覽器訪問 http://127.0.0.1:8000/docs
    print("請打開瀏覽器測試：http://127.0.0.1:8000/docs")
    print("伺服器啟動中... 請至 http://127.0.0.1:8000/docs 進行測試")
    uvicorn.run("form_file_handler:app", host="127.0.0.1", port=8000, reload=True)