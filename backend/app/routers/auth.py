from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from fastapi import APIRouter, BackgroundTasks, HTTPException
from datetime import timedelta
from ..utils.email import send_password_reset_email
from ..models import User
from ..utils.security import get_current_active_user
from ..database import SessionDep, Depends
from ..schemas.auth import RESET_TOKEN_EXPIRE_MINUTES, ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserResponse, Token, UserLogin, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_PASSWORD_SECRET_KEY,ALGORITHM
from ..crud.auth import create_reset_token, get_hashed_password, get_user_by_email, verify_password, create_access_token, update_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate, session: SessionDep) -> UserResponse:
    existed = await get_user_by_email(email=user.email, session=session)
    if existed:
        raise HTTPException(status_code=400, detail="User existed")
    user_data = user.model_dump() # Lấy data dạng dict
    raw_password = user_data.pop("password") # Rút password ra và xóa khỏi dict
    user_data["hashed_password"] = get_hashed_password(password=raw_password) # Thêm hash vào đúng tên cột
    user_db = User(**user_data) # Bây giờ mới ném vào Model
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = await get_user_by_email(email=form_data.username, session=session)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, session: SessionDep):
    user = await get_user_by_email(email = request.email, session=session)
    if not user:
        return {"detail": "If the email exists, a reset link has been sent."}
    reset_token_expires = timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    reset_token = create_reset_token(
        data={"sub": request.email, "pwd_hash": user.hashed_password}, expires_delta=reset_token_expires
    )

    background_tasks.add_task(send_password_reset_email, request.email, reset_token)
    
    return {"detail": "If the email exists, a reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, session: SessionDep):
    # 1. Decode token
    try:
        payload = jwt.decode(request.reset_token, RESET_PASSWORD_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        pwd_hash_in_token = payload.get("pwd_hash")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    # 2. Lấy user từ DB
    user = await get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Check xem token này đã cũ chưa (nếu mật khẩu đã bị đổi rồi thì pwd_hash trong DB sẽ khác trong token)
    if user.hashed_password != pwd_hash_in_token:
        raise HTTPException(status_code=400, detail="Token has expired or already used")

    # 4. Update pass mới
    await update_password(session=session, user=user, new_password=request.new_password)
    
    return {"detail": "Password updated successfully"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user