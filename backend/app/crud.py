from sqlalchemy.orm import Session
from app import models, schemas

# Récupérer tous les CV à corriger (status 'pending')
def get_pending_extractions(db: Session):
    return db.query(models.CVExtraction).filter(models.CVExtraction.status == "pending").all()

# Récupérer un CV spécifique par son ID
def get_extraction(db: Session, extraction_id: int):
    return db.query(models.CVExtraction).filter(models.CVExtraction.id == extraction_id).first()

# Enregistrer la correction humaine
def update_extraction(db: Session, extraction_id: int, correction: schemas.CVExtractionUpdate):
    db_item = db.query(models.CVExtraction).filter(models.CVExtraction.id == extraction_id).first()
    if db_item:
        # On met à jour tous les champs fournis par React
        for key, value in correction.dict().items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
    return db_item