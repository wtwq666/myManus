# 导入FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
import asyncpg
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接参数
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mymanus")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PORT = os.getenv("DB_PORT", "5432")

# 全局数据库连接对象
db_connection = None

async def create_db_connection():
    """创建数据库连接"""
    try:
        # 使用从环境变量加载的参数
        conn_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DB_NAME", "mymanus"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "your_password_here")
        }
        
        print("\n使用以下参数创建数据库连接:")
        for key, value in conn_params.items():
            if key == "password":
                print(f"- {key}: {'*' * len(value)}")
            else:
                print(f"- {key}: {value}")
        
        # 尝试创建数据库连接
        print("\n尝试创建数据库连接...")
        
        # 使用asyncpg创建异步连接
        conn = await asyncpg.connect(**conn_params)
        print("✅ 使用asyncpg成功连接到PostgreSQL数据库!")
        return conn
    
    except Exception as e:
        print(f"\n❌ 无法连接到PostgreSQL数据库: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_connection
    # 应用启动时执行的代码
    print("应用启动")
    # 注意：不再在启动时自动创建数据库连接，避免连接失败导致应用无法启动
    yield
    # 应用关闭时执行的代码
    print("应用关闭")
    # 关闭数据库连接
    if db_connection:
        await db_connection.close()
        print("✅ 数据库连接已关闭")


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()

# 添加测试数据库连接的路由
@api_router.get("/test-db-connection")
async def test_db_connection():
    """测试数据库连接"""
    global db_connection
    try:
        if db_connection is None:
            db_connection = await create_db_connection()
            if db_connection:
                return {"status": "success", "message": "✅ 成功连接到PostgreSQL数据库!"}
            else:
                return {"status": "error", "message": "❌ 无法连接到PostgreSQL数据库"}
        else:
            return {"status": "success", "message": "✅ 数据库连接已存在!"}
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





