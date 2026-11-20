"""Database setup. The app talks to Postgres (Neon) through DATABASE_URL."""
import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()  # reads a local .env file if there is one (never committed to Git)


class Base(DeclarativeBase):
    pass


class NoteRow(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)


def database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Put your Neon connection string in .env")
    # Neon gives postgresql://... ; SQLAlchemy needs to be told to use the psycopg driver.
    return url.replace("postgresql://", "postgresql+psycopg://", 1)


@lru_cache
def get_engine():
    # pool_pre_ping: Neon sleeps when idle, so check the connection before using it.
    return create_engine(database_url(), pool_pre_ping=True)


def get_session():
    with Session(get_engine()) as session:
        yield session

