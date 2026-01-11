from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


import os

# On récupère le chemin absolu du dossier où se trouve ce fichier (backend/app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# On remonte d'un niveau pour mettre le .db dans /backend
DB_PATH = os.path.join(BASE_DIR, "..", "cv_extractions.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"
# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # nécessaire pour SQLite + FastAPI
)

# Session locale
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base SQLAlchemy
Base = declarative_base()


# Dépendance FastAPI pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
