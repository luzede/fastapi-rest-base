### IMPORTS ###
# External Libraries
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime, time, date, timedelta


# Internal Libraries
from app.example.constants import Type, Color


### CODE ###


class FoxBase(BaseModel):
    name: str
    age: int


class FoxCreate(FoxBase):
    # FastAPI will know that the value of "type" and "color" is not required because of the default value = None.
    # The Optional in Optional[str] is not used by FastAPI, but will allow your editor to give you better support and detect errors.
    type: Type | None = None
    color: Color | None = None


class Fox(FoxBase):
    id: int
    type: Type
    color: Color
    ## This field throws a greenlet error when returning a models.Fox instance
    ## whose awaitable attribute/lazy-loaded attribute has not been explicitly awaited/loaded
    ## so I removed it from the pydantic model
    # jumped_over: List["Dog"] | None = None

    # "orm_mode" has been renamed to "from_attributes" in V2 of Pydantic
    model_config = ConfigDict(from_attributes=True)


class DogBase(BaseModel):
    name: str
    age: int


class DogCreate(DogBase):
    type: Type | None = None
    color: Color | None = None


class Dog(DogBase):
    id: int
    type: Type
    color: Color
    # jumped_over_by: List["Fox"] | None = None

    model_config = ConfigDict(from_attributes=True)


class FoxDogLink(BaseModel):
    fox_id: int
    dog_id: int


class ExampleBase(BaseModel):
    string: str


class ExampleCreate(ExampleBase):
    integer: int | None = None
    float_num: float | None = None
    datetime_obj: datetime | None = None
    time_obj: time | None = None
    date_obj: date | None = None
    timedelta_obj: timedelta | None = None


class Example(ExampleBase):
    uuid: UUID
    integer: int
    float_num: float
    datetime_obj: datetime
    time_obj: time
    date_obj: date
    timedelta_obj: timedelta

    model_config = ConfigDict(from_attributes=True)
