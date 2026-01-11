from sqlalchemy.orm import Session
from app import models, schemas

# Fetch all CVs with status 'pending'
def get_pending_extractions(db: Session):
    return db.query(models.CVExtraction).filter(models.CVExtraction.status == "pending").all()

# Fetch a single CV using its ID
def get_extraction(db: Session, extraction_id: int):
    return db.query(models.CVExtraction).filter(models.CVExtraction.id == extraction_id).first()

# Save human corrections 
def update_extraction(db: Session, extraction_id: int, correction: schemas.CVExtractionUpdate):
    # # Find the record by ID
    db_item = db.query(models.CVExtraction).filter(models.CVExtraction.id == extraction_id).first()
    if db_item:
        # update the database fields
        for key, value in correction.dict().items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
    return db_item