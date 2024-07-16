### IMPORTS ###
# External Libraries
from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from uuid import UUID


# Internal Libraries
from app.example import schemas, models
from app.database import get_session


### CODE ###

router = APIRouter()


@router.get("/foxes", response_model=List[schemas.Fox], status_code=status.HTTP_200_OK)
async def get_foxes(session: AsyncSession = Depends(get_session)):
    query_res = await session.execute(statement=select(models.Fox))
    return query_res.scalars().all()


@router.get("/foxes/{id}", response_model=schemas.Fox, status_code=status.HTTP_200_OK)
async def get_fox(id: int, session: AsyncSession = Depends(get_session)):
    fox = await session.get_one(models.Fox, id)
    return fox


@router.post("/foxes", response_model=schemas.Fox, status_code=status.HTTP_201_CREATED)
async def create_fox(
    fox: schemas.FoxCreate, session: AsyncSession = Depends(get_session)
):
    new_fox = models.Fox(**fox.model_dump())
    session.add(new_fox)
    await session.commit()
    # A lazy-loaded relationship can be loaded explicitly under asyncio using AsyncSession.refresh()
    # and specifying the attribute name of the lazy-loaded relationship,
    # or like the example below using the awaitable attribute.
    # await session.refresh(new_fox, attribute_names=["jumped_over"])

    await session.refresh(new_fox)

    # If you need to access the jumped_over attribute, you need to await it
    # like this, since it is an awaitable attribute.
    # await new_fox.awaitable_attrs.jumped_over

    return new_fox


@router.get(
    "/foxes/{id}/jumped_over",
    response_model=List[schemas.Dog],
    status_code=status.HTTP_200_OK,
)
async def get_dogs_jumped_over_by_fox(
    id: int, session: AsyncSession = Depends(get_session)
):
    fox = await session.get_one(
        models.Fox,
        id,
    )
    return await fox.awaitable_attrs.jumped_over


@router.get("/dogs", response_model=List[schemas.Dog], status_code=status.HTTP_200_OK)
async def get_dogs(session: AsyncSession = Depends(get_session)):
    query_res = await session.execute(select(models.Dog))

    return query_res.scalars().all()


@router.get("/dogs/{id}", response_model=schemas.Dog, status_code=status.HTTP_200_OK)
async def get_dog(id: int, session: AsyncSession = Depends(get_session)):
    dog = await session.get_one(models.Dog, id)
    return dog


@router.post("/dogs", response_model=schemas.Dog, status_code=status.HTTP_201_CREATED)
async def create_dog(
    dog: schemas.DogCreate, session: AsyncSession = Depends(get_session)
):
    new_dog = models.Dog(**dog.model_dump())
    session.add(new_dog)
    await session.commit()
    await session.refresh(new_dog)

    return new_dog


@router.post("/fox_jumped_over_dog", status_code=status.HTTP_201_CREATED)
async def create_fox_dog_link(
    fox_dog_link: schemas.FoxDogLink, session: AsyncSession = Depends(get_session)
):
    # Checking if fox and the dog with the provided ids exist
    # if they don't, it will throw an exception
    _ = await session.get_one(models.Fox, fox_dog_link.fox_id)
    _ = await session.get_one(models.Dog, fox_dog_link.dog_id)
    new_fox_dog_link = models.FoxDogLink(**fox_dog_link.model_dump())
    session.add(new_fox_dog_link)
    await session.commit()


@router.get(
    "/examples", response_model=List[schemas.Example], status_code=status.HTTP_200_OK
)
async def get_examples(session: AsyncSession = Depends(get_session)):
    query_res = await session.execute(select(models.Example))
    return query_res.scalars().all()


@router.get(
    "/examples/{id}", response_model=schemas.Example, status_code=status.HTTP_200_OK
)
async def get_example(id: UUID, session: AsyncSession = Depends(get_session)):
    example = await session.get_one(models.Example, id)
    return example


@router.post(
    "/examples", response_model=schemas.Example, status_code=status.HTTP_201_CREATED
)
async def create_example(
    example: schemas.ExampleCreate, session: AsyncSession = Depends(get_session)
):
    new_example = models.Example(**example.model_dump())
    session.add(new_example)
    await session.commit()
    await session.refresh(new_example)

    return new_example
