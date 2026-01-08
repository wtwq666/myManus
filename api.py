# 导入FastAPI
from fastapi import FastAPI

# 创建FastAPI应用实例
app = FastAPI()

# 定义根路径的GET请求（访问http://127.0.0.1:8000会触发这个函数）
@app.get("/")
async def root():
    # 返回JSON响应（FastAPI会自动转成JSON）
    return {"message": "Hello FastAPI!"}