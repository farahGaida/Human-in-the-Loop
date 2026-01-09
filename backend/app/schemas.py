from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schéma de base partagé
class CVExtractionBase(BaseModel):
    cv_id: str
    predicted_name: Optional[str]
    predicted_email: Optional[str]
    predicted_phone: Optional[str]
    predicted_orgs: Optional[str]
    predicted_experience: Optional[str]
    predicted_education: Optional[str]
    status: str
    model_version: str

# Schéma pour mettre à jour (ce que React envoie quand on corrige)
class CVExtractionUpdate(BaseModel):
    corrected_name: str
    corrected_email: str
    corrected_phone: str
    corrected_orgs: str
    corrected_experience: str
    corrected_education: str
    correction_time_seconds: float
    status: str = "corrected" # Passe automatiquement à corrected

# Schéma complet pour la lecture (ce que l'API renvoie)
class CVExtraction(CVExtractionBase):
    id: int
    raw_text: str
    corrected_name: Optional[str]
    corrected_email: Optional[str]
    corrected_phone: Optional[str]
    corrected_orgs: Optional[str]
    corrected_experience: Optional[str]
    corrected_education: Optional[str]
    correction_time_seconds: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Permet de convertir SQLAlchemy vers Pydantic