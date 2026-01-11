from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "cv_extractions.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"
# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

# Configure the database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#  SQLAlchemy Base
Base = declarative_base()


# FastAPI dependency to provide a database session to routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
