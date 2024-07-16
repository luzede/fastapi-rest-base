### IMPORTS ###
# External Libraries
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from sqlalchemy.exc import IntegrityError

# Internal Libraries
from app.auth import models, schemas
from app.auth.config import auth_config
from app.database import get_session
from app.auth.exceptions import user_not_found, wrong_password, user_already_registered
from app.auth.utils import create_access_token
from app.auth.dependencies import get_current_user
from typing import Annotated


### CODE ###

router = APIRouter()


@router.post(
    "/api/token", response_model=schemas.Token, status_code=status.HTTP_201_CREATED
)
async def login_for_access_token(
    # You cannot do "format_data: OAuth2PasswordRequestForm", it needs to be this way with
    # annotated and depends with no arguments
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await session.get_one(models.User, form_data.username)
    except Exception:
        raise user_not_found

    if not bcrypt.checkpw(
        form_data.password.encode(encoding="utf-8"),
        user.password_hash.encode(encoding="utf-8"),
    ):
        raise wrong_password

    access_token = create_access_token(user.username, auth_config.JWT_EXPIRE)
    return schemas.Token(access_token=access_token, token_type="Bearer")


@router.post(
    "/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
async def create_user(
    data: schemas.UserCreate, session: AsyncSession = Depends(get_session)
):
    username = data.username
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(data.password.encode(), salt)

    new_user = models.User(
        username=username, salt=salt.decode(), password_hash=password_hash.decode()
    )
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError:
        raise user_already_registered()
    return new_user


@router.get("/users/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_current_user(user: schemas.User = Depends(get_current_user)):
    return user
