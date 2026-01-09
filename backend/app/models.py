from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.database import Base


Base = declarative_base()

class CVExtraction(Base):
    __tablename__ = "extractions"

    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(String, unique=True, index=True)
    raw_text = Column(Text)

    # --- Champs prédits par l'IA ---
    predicted_name = Column(String)
    predicted_email = Column(String)
    predicted_phone = Column(String)
    predicted_orgs = Column(String)
    predicted_experience = Column(Text)
    predicted_education = Column(Text)

    # --- Champs corrigés par l'Humain ---
    corrected_name = Column(String, nullable=True)
    corrected_email = Column(String, nullable=True)
    corrected_phone = Column(String, nullable=True)
    corrected_orgs = Column(String, nullable=True)
    corrected_experience = Column(Text, nullable=True)
    corrected_education = Column(Text, nullable=True)

    # --- MLOps metadata ---
    model_version = Column(String, default="v1")
    status = Column(String, default="pending")  # pending / corrected / validated
    auto_accepted = Column(Integer, default=0)

    correction_time_seconds = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
