# External Libraries
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.schema import ForeignKey
from uuid import UUID, uuid4
from datetime import datetime, time, timedelta, date, timezone
import random
from typing import List
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE


# Internal Libraries
from app.models import Base
from app.example.constants import Type, Color


# default type mapping, deriving the type for mapped_column()
# from a Mapped[] annotation
# type_map: Dict[Type[Any], TypeEngine[Any]] = {
#     bool: types.Boolean(),
#     bytes: types.LargeBinary(),
#     datetime.date: types.Date(),
#     datetime.datetime: types.DateTime(),
#     datetime.time: types.Time(),
#     datetime.timedelta: types.Interval(),
#     decimal.Decimal: types.Numeric(),
#     float: types.Float(),
#     int: types.Integer(),
#     str: types.String(),
#     uuid.UUID: types.Uuid(),
# }


# Useful link about server_default and default parameters of mapped_column:
# https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#defaults-default-factory-insert-default


class Example(Base):
    __tablename__ = "examples"
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    integer: Mapped[int] = mapped_column(autoincrement=True)
    float_num: Mapped[float] = mapped_column(name="float", default=random.random)
    string: Mapped[str]
    datetime_obj: Mapped[datetime] = mapped_column(
        DATETIME_TIMEZONE,  # I can also do DateTime(timezone=True)
        name="datetime",
        default=lambda: datetime.now(timezone.utc),
    )
    time_obj: Mapped[time] = mapped_column(
        name="time", default=lambda: datetime.now(timezone.utc).time()
    )
    date_obj: Mapped[date] = mapped_column(
        name="date", default=lambda: datetime.now(timezone.utc).date()
    )
    timedelta_obj: Mapped[timedelta] = mapped_column(
        name="timedelta", default=lambda: timedelta(days=random.random())
    )

    def __repr__(self) -> str:
        return f"<Example uuid={self.uuid}>"


class Fox(Base):
    __tablename__ = "foxes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    age: Mapped[int]
    # Randomly choose an enum value for the type, enums support iteration
    # but they are not a list to be indexed, so we need to convert them to a list
    # and then use the random.choice function to get one of the enums from the list
    type: Mapped[Type] = mapped_column(default=lambda: random.choice(list(Type)))
    color: Mapped[Color] = mapped_column(default=lambda: random.choice(list(Color)))
    # Useful link about 'secondary' parameter of relationship:
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-a-late-evaluated-form-for-the-secondary-argument-of-many-to-many
    # It is for when we define the link/association table later than the models to be linked
    # either way, it is better to pass classes/lambdas than a string
    jumped_over: Mapped[List["Dog"]] = relationship(
        "Dog",
        back_populates="jumped_over_by",
        # secondary has to be a Table object, not a mapped class
        # fortunately, mapped class provides a __table__ attribute
        # that returns the Table object
        # otherwise I would have to delete the mapped class and define a Table object
        secondary=lambda: FoxDogLink.__table__,
        passive_deletes=True,
        passive_updates=True,
    )

    def __str__(self) -> str:
        return f"The {self.type} {self.color} fox named {self.name}"

    def __repr__(self) -> str:
        return f"<Fox name={self.name} type={self.type} color={self.color}>"


class Dog(Base):
    __tablename__ = "dogs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    age: Mapped[int]
    type: Mapped[Type] = mapped_column(default=lambda: random.choice(list(Type)))
    color: Mapped[Color] = mapped_column(default=lambda: random.choice(list(Color)))
    # 'passive_deletes=True' means that there is an ON DELETE CASCADE on the foreign key
    # so it no longer has to load the collection to mark the items as deleted in the
    # link/association table, database will take care of it
    # Same goes with 'passive_updates=True' for ON UPDATE CASCADE
    jumped_over_by: Mapped[List["Fox"]] = relationship(
        "Fox",
        back_populates="jumped_over",
        secondary=lambda: FoxDogLink.__table__,
        passive_deletes=True,
        passive_updates=True,
    )

    def __str__(self) -> str:
        return f"The {self.type} {self.color} fox named {self.name}"

    def __repr__(self) -> str:
        return f"<Dog name={self.name} type={self.type} color={self.color}>"


class FoxDogLink(Base):
    __tablename__ = "fox_dog_links"
    fox_id: Mapped[int] = mapped_column(
        ForeignKey("foxes.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    dog_id: Mapped[int] = mapped_column(
        ForeignKey("dogs.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
