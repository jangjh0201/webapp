import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from models.schemas import FAKE_USERS_DB, User
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

SECRET = os.getenv("SECRET_KEY")
manager = LoginManager(SECRET, token_url="/auth/token", use_cookie=True)


@manager.user_loader()
def load_user(username: str):
    user = FAKE_USERS_DB.get(username)
    if user:
        return User(**user)


def authenticate_user(username: str, password: str):
    user = load_user(username)
    if not user or user.password != password:
        return None
    return user
