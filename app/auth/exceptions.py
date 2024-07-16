from fastapi.exceptions import HTTPException
from fastapi import status


user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
    headers={"WWW-Authenticate": "Bearer"},
)


wrong_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong password",
    headers={"WWW-Authenticate": "Bearer"},
)


user_already_registered = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
)
