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
    total = db.query(models.CVExtraction).count()
    
    # Récupération de tous les CV validés
    validated_cvs_list = db.query(models.CVExtraction).filter(
        models.CVExtraction.status == "validated"
    ).all()
    
    corrected_count = len(validated_cvs_list)

    # Métriques granulaires
    cv_with_errors = 0      # Nombre de CV impactés
    total_fields_fixed = 0  # Nombre total de champs modifiés

    for cv in validated_cvs_list:
        field_errors = 0
        # On compare chaque champ important
        if cv.predicted_name != cv.corrected_name:
            field_errors += 1
        if cv.predicted_orgs != cv.corrected_orgs:
            field_errors += 1
        # Tu peux ajouter ici phone ou email si tu veux les compter
        
        if field_errors > 0:
            cv_with_errors += 1
            total_fields_fixed += field_errors
    
    # Calcul du temps moyen
    avg_time = db.query(func.avg(models.CVExtraction.correction_time_seconds)).filter(
        models.CVExtraction.status == "validated"
    ).scalar() or 0

  
    
    

    return {
        "total": total,
        "corrected": corrected_count,
        "actual_changes": cv_with_errors,         # Nb de documents corrigés
        "total_fields_fixed": total_fields_fixed, # Nb total de champs rectifiés
        "avg_time": round(avg_time, 2),
    }