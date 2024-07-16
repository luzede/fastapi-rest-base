# LOCAL CONFIGS FOR AUTHENTICATION
### IMPORTS ###
# External Libraries
from pydantic_settings import BaseSettings

# Internal Libraries


### CODE ###


class AuthConfig(BaseSettings):
    JWT_SECRET: str = "example"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE: int = 5  # minutes


auth_config = AuthConfig()
