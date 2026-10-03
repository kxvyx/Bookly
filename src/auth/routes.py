from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta

REFRESH_TOKEN_EXPIRY = 172800

auth_router = APIRouter()
user_service = UserService()

@auth_router.post('/signup' , response_model=UserModel , status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User with this email already exists")

    new_user = await user_service.create_user(user_data,session)
    return new_user

@auth_router.post('/login')
async def login_users(login_data:UserLoginModel,session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user:
        password_valid = verify_password(password,user.password_hash)

        if password_valid:
            user_data = {
                "email": user.email,
                "user_uid": str(user.uid),
            }

            access_token = create_access_token(user_data)
            refresh_token = create_access_token(user_data, expiry=timedelta(seconds=REFRESH_TOKEN_EXPIRY), resfresh=True)

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":user_data
                }
            )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")