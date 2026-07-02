from fastapi import Depends, HTTPException
from typing import Annotated
from ..crud.auth import get_user_by_email
from ..database import SessionDep
from ..schemas.auth import SECRET_KEY, ALGORITHM
from ..models import User
import jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
credentials_exception = HTTPException(status_code=401, detail = "Error")

async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    # 3. Dùng email để tìm User trong DB
    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
