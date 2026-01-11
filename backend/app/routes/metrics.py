from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/")
def get_metrics(db: Session = Depends(get_db)):
    # Get the total number of CVs
    total = db.query(models.CVExtraction).count()
    
    # Get all CVs with 'validated' status
    validated_cvs_list = db.query(models.CVExtraction).filter(
        models.CVExtraction.status == "validated"
    ).all()
    
    corrected_count = len(validated_cvs_list)

    # Variables to track errors found during human review
    cv_with_errors = 0      # Number of CVs that needed at least one fix
    total_fields_fixed = 0  # Total count of all corrected fields

    for cv in validated_cvs_list:
        field_errors = 0
        # Compare AI prediction vs human correction
        if cv.predicted_name != cv.corrected_name:
            field_errors += 1
        if cv.predicted_orgs != cv.corrected_orgs:
            field_errors += 1
        
        # If the CV has errors, increment the counters
        if field_errors > 0:
            cv_with_errors += 1
            total_fields_fixed += field_errors
    
    # Calculate average correction time
    avg_time = db.query(func.avg(models.CVExtraction.correction_time_seconds)).filter(
        models.CVExtraction.status == "validated"
    ).scalar() or 0

  
    
    
    # Return data as a dictionary for the frontend
    return {
        "total": total,
        "corrected": corrected_count,
        "actual_changes": cv_with_errors,         # Nb of documents modified
        "total_fields_fixed": total_fields_fixed, # Nb of individual fields fixed
        "avg_time": round(avg_time, 2),
    }