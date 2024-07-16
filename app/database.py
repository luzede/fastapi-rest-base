### IMPORTS ###

# External Libraries
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy.engine.url import URL
from collections.abc import AsyncGenerator

# Internal Libraries
from app.config import database_config as db_config

### CODE ###

# Database URL, based on the configuration
url = URL(
    drivername=db_config.DB_DRIVERNAME,
    username=db_config.DB_USERNAME,
    password=db_config.DB_PASSWORD,
    host=db_config.DB_HOST,
    port=db_config.DB_PORT,
    database=db_config.DB_NAME,
    # setting "'sslmode': 'require'" does not work in the query parameter
    # it errors while running alembic migrations
    query={},
)

# connect_args={"sslmode": "require"}, this argument is also not working
engine = create_async_engine(url=url, echo=True)

AsyncSessionFactory = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Get a session from the SessionFactory variable from 'app/database.py' which is one of the following type:
    async_sessionmaker[AsyncSession]

    :return: a session of type AsyncSession
    """

    # Creates a session and takes care of closing it when the context manager is done
    async with AsyncSessionFactory() as session:
        yield session
