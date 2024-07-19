# FastAPI REST Base App
It was annoying to configure from the start for every project and go through configurations and documentation each time I started a project so I created this base starting point which significantly speeds up development time. I followed all the best practices I found on the internet, took inspiration about the folder structure and best practices of this repo ["fastapi best practices"](https://github.com/zhanymkanov/fastapi-best-practices)

The base is built using **asyncpg+postgresql** in mind as a database, you can use a different database driver that supports asynchronous operations. I want it to be async.

The folder structure is the following:
```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   └── example
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── database.py  # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── example
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
└── alembic.ini
```
For more information why I picked this kind of structure you can check out the repository I linked above and read it, it is very informative.

# Installing
I will keep it short
```bash
git clone ...
cd ./fastapi_project
python -m venv .venv
source .venv/bin/activate # If Mac/Linux
source .venv/Scripts/activate # If Windows
pip install -r requirements/dev.txt

# Before you run this command, you need
# to setup up the environmental variables
# See example in ".env.example" file
alembic upgrade head

# To start the app run the following:
uvicorn app.main:app --host localhost --port 3000 
```

I have implemented JWT authentication in the `auth` folder and created different types of models and schemas to easily recall how to do this and that with `SQLAlchemy`.

# Configuring the `.env` file
As in the `.env.example` file, you need to configure these fields before you are able to start the application. You can rename `.env.example` to `.env` or just create a new one. `DB_DRIVERNAME` always has to be async, because migrations uses an async configured template.
```bash
### DATABASE ###
DB_USERNAME=example
DB_PASSWORD=example
DB_HOST=localhost
DB_PORT=None  # None if you do not need to specify the port number
DB_NAME=example
# It has to be async, no matter what database you use, PostgreSQL is recommended
DB_DRIVERNAME=postgresql+asyncpg

  

### JWT ###
JWT_SECRET  =  "example"
JWT_ALGORITHM  =  HS256
JWT_EXPIRE  =  5  # minutes
```

# Migrations
To be able to do migrations easily, you just edit the models and then using alembic automatically generate it:
```bash
alembic revision --autogenerate -m "message"
# and then you can run to apply the latest migrations
alembic upgrade head 
# To downgrade you use the command
alembic downgrade -1 # To go back one migration
alembic downgrade -N # where N is a number specifying how far back it should go
```
