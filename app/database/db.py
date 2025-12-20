from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys

# 处理打包成exe后的路径问题
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe，数据库保存在exe所在目录
    base_path = os.path.dirname(sys.executable)
else:
    # 如果是开发环境，数据库保存在项目根目录
    base_path = os.path.join(os.path.dirname(__file__), '..', '..')
    base_path = os.path.abspath(base_path)

DB_PATH = os.path.join(base_path, 'database.db')
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    # Import models to register them with Base metadata
    from . import models_db as _models
    Base.metadata.create_all(bind=engine)

