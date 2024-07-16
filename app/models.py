### IMPORTS ###

# External Libraries
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# Internal Libraries


### CODE ###


class Base(AsyncAttrs, DeclarativeBase):
    pass
