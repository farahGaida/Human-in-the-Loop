import sys
from pathlib import Path

# Ajout de la racine du projet au PATH
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

# Imports depuis le backend
from backend.app.database import SessionLocal, engine
from backend.app.models import Base, CVExtraction

# Imports depuis le module ML
from ml.extraction.extract_fields import (
    extract_name_spacy, 
    extract_email, 
    extract_phone, 
    extract_orgs_spacy, 
    extract_section
)

def seed():
    # Crée les tables si elles n'existent pas encore
    print("🛠️ Vérification des tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    # On ajuste le chemin vers data/text depuis la racine
    text_folder = root_path / "data" / "text"
    
    if not text_folder.exists():
        print(f"❌ Erreur : Le dossier {text_folder} est introuvable.")
        return

    cv_files = list(text_folder.glob("*.txt"))
    print(f"📂 {len(cv_files)} fichiers trouvés dans {text_folder}")

    for txt_file in cv_files:
        if db.query(CVExtraction).filter(CVExtraction.cv_id == txt_file.stem).first():
            print(f"⏩ {txt_file.name} déjà présent, on passe.")
            continue
            
        print(f"🧠 Analyse de {txt_file.name} via SpaCy...")
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
    print("✅ Terminé ! Base de données prête pour le Frontend.")

if __name__ == "__main__":
    seed()