import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

# Backend imports for database management
from backend.app.database import SessionLocal, engine
from backend.app.models import Base, CVExtraction

# ML imports for entity and section extraction
from ml.extraction.extract_fields import (
    extract_name_spacy, 
    extract_email, 
    extract_phone, 
    extract_orgs_spacy, 
    extract_section
)

def seed():
    # Create database tables if they don't exist
    print("🛠️ checking tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    # Define the path to the extracted text files
    text_folder = root_path / "data" / "text"
    
    if not text_folder.exists():
        print(f"❌ Error : folder {text_folder} not found")
        return

    # List all .txt files in the folder
    cv_files = list(text_folder.glob("*.txt"))
    print(f"📂 found {len(cv_files)} fiels in {text_folder}")

    for txt_file in cv_files:
        if db.query(CVExtraction).filter(CVExtraction.cv_id == txt_file.stem).first():
            print(f"⏩ {txt_file.name} already exists, skipping")
            continue
            
        print(f"🧠 Analyzing {txt_file.name} with SpaCy...")
        text = txt_file.read_text(encoding="utf-8", errors="ignore")
        
        new_cv = CVExtraction(
            cv_id=txt_file.stem,
            raw_text=text,
            predicted_name=extract_name_spacy(text),
            predicted_email=extract_email(text),
            predicted_phone=extract_phone(text),
            predicted_orgs=extract_orgs_spacy(text),
            predicted_experience=extract_section(text, ["experience"], ["education", "skills"]),
            predicted_education=extract_section(text, ["education"], ["experience", "skills"]),
            status="pending",
            model_version="v1"
        )
        
        db.add(new_cv)
    
    db.commit()
    db.close()
    print("✅ Done! Database is ready for the Frontend")

if __name__ == "__main__":
    seed()