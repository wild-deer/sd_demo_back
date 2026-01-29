from fastapi import APIRouter, HTTPException, Body, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/db", tags=["Database"])

# 数据库配置
DB_USER = "865735712"
DB_PASS = "!YJLs13981383032"
DB_HOST = "192.168.124.8"
DB_PORT = "15432"
DB_NAME = "865735712"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建数据库引擎
try:
    engine = create_engine(DATABASE_URL)
    logger.info(f"Database engine created for {DB_HOST}:{DB_PORT}/{DB_NAME}")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    engine = None

@router.post("/execute_sql")
def execute_sql_endpoint(sql: str = Form(..., description="要执行的 SQL 语句")):
    """
    执行 Postgres SQL 语句。
    注意：此接口允许执行任意 SQL，请谨慎使用。
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Database engine not initialized")
    
    sql_query = sql.strip()
    logger.info(f"Received SQL query: {sql_query}")
    if not sql_query:
        raise HTTPException(status_code=400, detail="SQL query cannot be empty")

    try:
        with engine.connect() as connection:
            # 使用 text() 包装 SQL 语句
            result = connection.execute(text(sql_query))
            
            # 判断是否是查询语句 (SELECT)
            # 简单的判断，实际情况可能更复杂（如 CTE），但对于基本用途足够
            if sql_query.lstrip().upper().startswith("SELECT") or sql_query.lstrip().upper().startswith("WITH"):
                keys = result.keys()
                rows = [dict(zip(keys, row)) for row in result.fetchall()]
                return {
                    "status": "success",
                    "type": "query",
                    "count": len(rows),
                    "data": rows
                }
            else:
                # 对于非查询语句 (INSERT, UPDATE, DELETE 等)，提交事务
                connection.commit()
                return {
                    "status": "success",
                    "type": "modification",
                    "rowcount": result.rowcount
                }
                
    except SQLAlchemyError as e:
        logger.error(f"SQL execution error: {e}")
        # 返回具体的错误信息以便调试
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
