import hashlib
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import User
import jwt
from datetime import datetime, timedelta, timezone
from ..schemas.auth import SECRET_KEY, RESET_PASSWORD_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_TOKEN_EXPIRE_MINUTES

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

def get_hashed_password(password: str) -> str:
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    hashed = bcrypt.hashpw(sha256_hash.encode('utf-8'), bcrypt.gensalt())

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    
    return bcrypt.checkpw(
        sha256_hash.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_reset_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, RESET_PASSWORD_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def update_password(session: AsyncSession, user: User, new_password: str):
    new_hashed_password = get_hashed_password(password=new_password)
    user.hashed_password = new_hashed_password
    await session.commit()
    await session.refresh(user)
