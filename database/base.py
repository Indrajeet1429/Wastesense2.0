import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

if not DATABASE_PASSWORD:
    raise RuntimeError("DATABASE_PASSWORD is not configured.")


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={"password": DATABASE_PASSWORD},
    pool_pre_ping=True,
)
