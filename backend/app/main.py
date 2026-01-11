from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import extractions, metrics 
from app.database import engine
from app.models import Base
from fastapi.staticfiles import StaticFiles

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Human-in-the-Loop CV Extraction",
    description="FastAPI backend for human correction and MLOps tracking",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="../data/raw_cvs"), name="static")

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def root():
    return {
        "message": "Human-in-the-Loop API is running "
        
    }
app.include_router(extractions.router)
app.include_router(metrics.router)
