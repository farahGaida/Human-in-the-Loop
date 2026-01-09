from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/")
def get_metrics(db: Session = Depends(get_db)):
    total = db.query(models.CVExtraction).count()
    corrected = db.query(models.CVExtraction).filter(
        models.CVExtraction.status == "validated"
    ).count()
    
    # Calcul du temps moyen de correction
    avg_time = db.query(func.avg(models.CVExtraction.correction_time_seconds)).filter(
        models.CVExtraction.status == "validated"
    ).scalar() or 0

    # Calcul du taux d'acceptation automatique
    auto_accepted_count = db.query(models.CVExtraction).filter(
        models.CVExtraction.auto_accepted == 1
    ).count()
    
    auto_accepted_pct = (auto_accepted_count / total * 100) if total > 0 else 0

    return {
        "total": total,
        "corrected": corrected,
        "avg_time": round(avg_time, 2),
        "auto_accepted": round(auto_accepted_pct, 2)
    }