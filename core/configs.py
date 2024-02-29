from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic_settings import BaseSettings

URL_DATABASE = 'postgresql+asyncpg://postgres:1234@localhost:5432/ControleDeResmas'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()

TEMPLATES = Jinja2Templates(directory='templates')
MEDIA = Path('media')

