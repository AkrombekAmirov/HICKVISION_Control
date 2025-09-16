from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import environ

load_dotenv()

DATABASE_URL = environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
