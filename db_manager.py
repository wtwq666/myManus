import asyncpg
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接参数
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "mymanus"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "your_password_here")
}

# 全局连接池对象
connection_pool = None

async def init_db_pool():
    """初始化数据库连接池"""
    global connection_pool
    try:
        print("正在初始化数据库连接池...")
        # 打印连接参数（隐藏密码）
        print("数据库连接参数:")
        for key, value in DB_CONFIG.items():
            if key == "password":
                print(f"- {key}: {'*' * len(value)}")
            else:
                print(f"- {key}: {value}")
        
        # 创建连接池
        connection_pool = await asyncpg.create_pool(**DB_CONFIG)
        print("✅ 数据库连接池初始化成功!")
        return connection_pool
    except Exception as e:
        print(f"❌ 数据库连接池初始化失败: {type(e).__name__}: {e}")
        return None

async def get_db_connection():
    """从连接池获取数据库连接"""
    global connection_pool
    if connection_pool is None:
        print("⚠️ 数据库连接池未初始化，正在尝试初始化...")
        await init_db_pool()
    
    if connection_pool:
        try:
            conn = await connection_pool.acquire()
            return conn
        except Exception as e:
            print(f"❌ 获取数据库连接失败: {type(e).__name__}: {e}")
            return None
    else:
        print("❌ 数据库连接池不可用")
        return None

async def release_db_connection(conn):
    """释放数据库连接回连接池"""
    global connection_pool
    if conn and connection_pool:
        try:
            await connection_pool.release(conn)
        except Exception as e:
            print(f"❌ 释放数据库连接失败: {type(e).__name__}: {e}")

async def close_db_pool():
    """关闭数据库连接池"""
    global connection_pool
    if connection_pool:
        try:
            await connection_pool.close()
            print("✅ 数据库连接池已关闭")
            connection_pool = None
        except Exception as e:
            print(f"❌ 关闭数据库连接池失败: {type(e).__name__}: {e}")

async def execute_query(query, *args):
    """执行SQL查询"""
    conn = None
    try:
        conn = await get_db_connection()
        if conn:
            result = await conn.fetch(query, *args)
            return result
    except Exception as e:
        print(f"❌ 执行查询失败: {type(e).__name__}: {e}")
        return None
    finally:
        await release_db_connection(conn)
