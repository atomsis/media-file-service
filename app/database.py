from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta,declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_media"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base: DeclarativeMeta = declarative_base()