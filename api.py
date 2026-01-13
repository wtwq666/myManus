# 导入FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行的代码
    print("应用启动")
    yield
    # 应用关闭时执行的代码
    print("应用关闭")


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()

from auth.api import router as auth_router
#用户认证模块
api_router.include_router(auth_router)

app.include_router(api_router,prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, 
    host="0.0.0.0", 
    port=8000
    )





