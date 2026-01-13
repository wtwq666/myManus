# 导入FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入数据库管理模块
from db_manager import init_db_pool, close_db_pool, get_db_connection, release_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行的代码
    print("应用启动")
    # 初始化数据库连接池
    await init_db_pool()
    yield
    # 应用关闭时执行的代码
    print("应用关闭")
    # 关闭数据库连接池
    await close_db_pool()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()

# 添加测试数据库连接的路由
@api_router.get("/test-db-connection")
async def test_db_connection():
    """测试数据库连接"""
    try:
        conn = await get_db_connection()
        if conn:
            await release_db_connection(conn)
            return {"status": "success", "message": "✅ 成功连接到PostgreSQL数据库!"}
        else:
            return {"status": "error", "message": "❌ 无法连接到PostgreSQL数据库"}
    except Exception as e:
        return {"status": "error", "message": f"❌ 数据库连接测试失败: {type(e).__name__}: {str(e)}"}

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





