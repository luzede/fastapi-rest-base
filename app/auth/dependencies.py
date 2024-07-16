### IMPORTS ###
# External Libraries
import jwt
from datetime import datetime, timezone
from typing import Any, Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession


# Internal Libraries
from app.auth.config import auth_config
from app.auth import schemas, models
from app.auth.exceptions import credentials_exception, user_not_found
from app.database import get_session

oauth = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_access_token_payload(
    # Only use Annotated for FastAPI dependencies,
    # For custom made things use "param: Type = Depends(dependency)"
    access_token: Annotated[str, Depends(oauth)],
) -> schemas.Payload:
    try:
        decoded_jwt: dict[str, Any] = jwt.decode(
            access_token, auth_config.JWT_SECRET, auth_config.JWT_ALGORITHM
        )
        # If JWT is expired, it will throw an error here, so we don't need to check
        # if the token expired or not later, everything is checked automatically here
        # and InvalidTokenError is base for ExpiredSignatureError so it will be caught
    except jwt.InvalidTokenError:
        raise credentials_exception

    username: str | None = decoded_jwt.get("sub")
    expire: int | None = decoded_jwt.get("exp")  # It returns time as Unix Timestamp

    if username is None:
        raise credentials_exception
    # "exp" in jwt token is Unix Timestamp in seconds (always from automatically)
    if expire is None:
        raise credentials_exception

    return schemas.Payload(
        sub=username,
        # fromtimestamp expects Unix Timepstamp in seconds,
        # if you have it in milliseconds, you have to divide it by 1000
        exp=datetime.fromtimestamp(expire, timezone.utc),
    )


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    payload: schemas.Payload = Depends(get_access_token_payload),
):
    try:
        user = await session.get_one(models.User, payload.sub)
    except Exception:
        raise user_not_found
    return user
