from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

# Đầu tiên là tạo 1 DB sau đó là kết nối
load_dotenv() # Load biến môi trường của DB
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL) # Tạo engine để kết nối với DB
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False) # Tạo các phiên làm việc

async def get_session():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

Base = declarative_base() # Model cha của các model con trong DB
