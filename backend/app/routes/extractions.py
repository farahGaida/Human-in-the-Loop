from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/extractions",
    tags=["extractions"]
)

# ROUTE 1 : Fetch all CVs that are waiting for human correction (status 'pending')
@router.get("/", response_model=List[schemas.CVExtraction])
def read_extractions(db: Session = Depends(get_db)):
    return crud.get_pending_extractions(db)

# ROUTE 2 : Fetch details of a specific CV
@router.get("/{extraction_id}", response_model=schemas.CVExtraction)
def read_extraction(extraction_id: int, db: Session = Depends(get_db)):
    db_extraction = crud.get_extraction(db, extraction_id)
    if db_extraction is None: 
        # if the ID doesn't exist
        raise HTTPException(status_code=404, detail="Extraction non trouvée")
    return db_extraction

# ROUTE 3 : receive and save human corrections from the React frontend
@router.post("/{extraction_id}/correct", response_model=schemas.CVExtraction)
def submit_correction(
    extraction_id: int, 
    correction: schemas.CVExtractionUpdate, 
    db: Session = Depends(get_db)
):
    # updates fields (predicted -> corrected) and changes status to 'validated'
    updated_item = crud.update_extraction(db, extraction_id, correction)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Erreur lors de la mise à jour")
    return updated_item