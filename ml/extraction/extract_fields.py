import re
import csv
import spacy
from pathlib import Path

# Charger spaCy
nlp = spacy.load("en_core_web_sm")

# Configuration des dossiers
TEXT_DIR = Path("data/text")
OUTPUT_DIR = Path("data/extracted")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_FILE = OUTPUT_DIR / "extractions_v1.csv"


# ---------------- REGEX ----------------

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "À corriger"


def extract_phone(text):
    # Ce regex cherche :
    # 1. Un éventuel + suivi de l'indicatif pays
    # 2. Des blocs de 2 à 4 chiffres séparés par des espaces, points ou tirets
    # 3. Il s'assure qu'il y a entre 8 et 15 chiffres au total
    phone_pattern = r"(?:(?:\+|00)[\s.-]?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}"
    
    match = re.search(phone_pattern, text)
    
    if match:
        phone = match.group(0).strip()
        # Sécurité : si le résultat est trop court (ex: juste une année 2024), on rejette
        if len(re.sub(r"\D", "", phone)) >= 8:
            return phone
            
    return "À corriger"

# ---------------- spaCy ----------------

def extract_name_spacy(text):
    doc = nlp(text[:1000])  # on limite pour la perf
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons[0] if persons else "Nom à corriger"


def extract_orgs_spacy(text):
    # On se concentre sur le début du CV (les 2000 premiers caractères) 
    # car l'employeur actuel est presque toujours en haut.
    doc = nlp(text[:2000])
    
    # On récupère les organisations, mais on ignore les mots trop courts ou suspects
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG" and len(ent.text) > 3]
    
    # On ne renvoie que la TOUTE PREMIÈRE organisation trouvée
    if orgs:
        return orgs[0]
    
    return "À corriger"


# ---------------- SECTIONS ----------------

def extract_section(text, keywords, stop_words):
    lines = text.split("\n")
    content = []
    capture = False
    stop_pattern = re.compile(r"|".join(stop_words), re.IGNORECASE)

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        if any(re.search(rf"\b{kw}\b", clean, re.IGNORECASE) for kw in keywords):
            capture = True
            continue

        if capture:
            if stop_pattern.search(clean) and len(clean.split()) < 4:
                break
            content.append(clean)

    return " | ".join(content[:8])


# ---------------- TRAITEMENT ----------------

rows = []

if not TEXT_DIR.exists():
    print(f"❌ Erreur : Le dossier {TEXT_DIR} n'existe pas.")
else:
    for txt_file in TEXT_DIR.glob("*.txt"):
        text = txt_file.read_text(encoding="utf-8", errors="ignore")

        row = {
            "cv_id": txt_file.stem,
            "name": extract_name_spacy(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "experience": extract_section(
                text,
                ["experience", "professional experience", "parcours"],
                ["education", "formation", "skills", "competences"]
            ),
            "education": extract_section(
                text,
                ["education", "formation", "cursus"],
                ["experience", "skills", "competences"]
            ),
            "organizations": extract_orgs_spacy(text)
        }

        rows.append(row)

# ---------------- SAUVEGARDE ----------------

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["cv_id", "name", "email", "phone", "experience", "education", "organizations"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Analyse terminée : {len(rows)} CV extraits → {OUTPUT_FILE}")
