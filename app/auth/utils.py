### IMPORTS ###
# External Libraries
import jwt
from datetime import timedelta, datetime, timezone


# Internal Libraries
from app.auth.config import auth_config


### CODE ###


def create_access_token(username: str, expire_in_minutes: int):
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_in_minutes),
    }
    encoded_jwt = jwt.encode(
        payload=payload, key=auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALGORITHM
    )
    return encoded_jwt
