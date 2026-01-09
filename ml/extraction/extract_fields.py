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
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\d{1,4}[-.\s]?){3,6}\d", text)
    return match.group(0).strip() if match else "À corriger"


# ---------------- spaCy ----------------

def extract_name_spacy(text):
    doc = nlp(text[:1000])  # on limite pour la perf
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons[0] if persons else "Nom à corriger"


def extract_orgs_spacy(text):
    doc = nlp(text)
    orgs = list(dict.fromkeys([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
    return " | ".join(orgs[:5])  # max 5 pour l'UI


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
