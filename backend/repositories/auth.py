from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.user import User
from pwdlib import PasswordHash
from datetime import timedelta, datetime
from jose import jwt, JWTError
from utils.settings import config

password_hash = PasswordHash.recommended()

def authenticate_user(
        username: str,
        password: str,
        db: AsyncSession = Depends(get_async_session)
        ):
    user = db.query(User).filter(user.username == username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Not authorized user or user not found in the system")
    if not password_hash.verify(password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect password")
    return user

def create_user_token(
        username: str, user_id: str, expires_delta: timedelta
        ):
    encode = {'sub': username, id: user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires}) 
    return jwt.encode(encode, config.SECURITY, algorithm=config.ALGORITHM)