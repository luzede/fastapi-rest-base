### IMPORTS ###
# External Libraries
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE
from datetime import datetime, timezone


# Internal Libraries
from app.models import Base


### CODE ###


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(unique=True, index=True, primary_key=True)
    password_hash: Mapped[str]
    # You can pass function to "default" parameter, "default_factory" does not work
    # "default_factory" can only be used when you use "MappedAsDataclass" mixin
    # Useful link: https://docs.sqlalchemy.org/en/20/orm/dataclasses.html
    salt: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DATETIME_TIMEZONE, default=lambda: datetime.now(tz=timezone.utc)
    )
