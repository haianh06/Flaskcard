from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
RESET_PASSWORD_SECRET_KEY = os.getenv("RESET_PASSWORD_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 5
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool    
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(min_length=8, max_length=50)