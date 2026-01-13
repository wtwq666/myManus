# 导入FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
import psycopg2
from psycopg2 import OperationalError
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

def create_db_connection():
    """创建数据库连接"""
    try:
        # 使用DSN格式连接
        dsn = "host=localhost dbname=mymanus user=postgres password=your_password_here port=5432"
        
        print(f"数据库连接DSN: host=localhost dbname=mymanus user=postgres password=****** port=5432")
        
        # 测试DSN的编码
        try:
            dsn.encode('utf-8')
            print("✅ DSN可以用UTF-8编码")
        except UnicodeEncodeError as e:
            print(f"❌ DSN无法用UTF-8编码: {e}")
        
        conn = psycopg2.connect(dsn)
        print("\n✅ 成功连接到PostgreSQL数据库!")
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
        db_connection.close()
        print("✅ 数据库连接已关闭")


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()

# 添加测试数据库连接的路由
@api_router.get("/test-db-connection")
def test_db_connection():
    """测试数据库连接"""
    global db_connection
    try:
        if db_connection is None:
            db_connection = create_db_connection()
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





