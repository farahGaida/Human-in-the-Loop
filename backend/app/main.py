from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import extractions, metrics 
from app.database import engine
from app.models import Base
from fastapi.staticfiles import StaticFiles

# Création des tables SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Human-in-the-Loop CV Extraction",
    description="Backend FastAPI pour correction humaine et suivi MLOps",
    version="1.0.0"
)
# Cette ligne permet d'accéder aux fichiers via http://localhost:8000/static/nom_du_cv.pdf
app.mount("/static", StaticFiles(directory="../data/raw_cvs"), name="static")

# CORS (nécessaire pour React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod → limiter
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def root():
    return {
        "message": "Human-in-the-Loop API is running 🚀"
        
    }
app.include_router(extractions.router)
app.include_router(metrics.router)
