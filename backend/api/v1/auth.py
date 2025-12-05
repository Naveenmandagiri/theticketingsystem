from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from db.db import get_async_session
from db.models.user import User
from db.schemas.user import CreateUserRequest, Token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pwdlib import PasswordHash
from typing import Annotated
from datetime import timedelta
from repositories.auth import authenticate_user, create_user_token

password_hash = PasswordHash.recommended()

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post('/')
async def create_user(userrequest: CreateUserRequest, 
                      db: AsyncSession = Depends(get_async_session)):
    create_user_model = User(
        username =  userrequest.username,
        password = password_hash.hash(userrequest.password)
    )
    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)
    return create_user_model

@auth_router.post("/token", response_model=Token)
async def login_for_accesstoken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: AsyncSession = Depends(get_async_session)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    token = create_user_token(user.username, user.id, timedelta(minutes=15))

    return {'access_token' : token, 'token_type' : 'bearer'}
