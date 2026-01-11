import re
import csv
import spacy
from pathlib import Path

# Load English spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Setup input/output directory paths
TEXT_DIR = Path("data/text")
OUTPUT_DIR = Path("data/extracted")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_FILE = OUTPUT_DIR / "extractions_v1.csv"


# ---------------- REGEX ----------------

def extract_email(text):
    # Regex pattern for standard email addresses
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "À corriger"


def extract_phone(text):
    # Regex for international and local phone numbers
    # Looks for country codes, optional spaces, dots, or dashes
    phone_pattern = r"(?:(?:\+|00)[\s.-]?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}"
    
    match = re.search(phone_pattern, text)
    
    if match:
        phone = match.group(0).strip()
        # ignore matches shorter than 8 digits (to avoid years like 2026)
        if len(re.sub(r"\D", "", phone)) >= 8:
            return phone
            
    return "À corriger"

# ---------------- spaCy ----------------

def extract_name_spacy(text):
    # Process only the first 1000 characters to improve speed
    doc = nlp(text[:1000])
    # Extract entities labeled as 'PERSON' 
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons[0] if persons else "Nom à corriger"


def extract_orgs_spacy(text):
    # Focus on the beginning of the CV where the current employer is usually listed
    doc = nlp(text[:2000])
    
    # Extract entities labeled as 'ORG' (organizations) and filter out very short strings
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG" and len(ent.text) > 3]
    
    # Return the first found organization
    if orgs:
        return orgs[0]
    
    return "À corriger"


# ---------------- SECTIONS ----------------

def extract_section(text, keywords, stop_words):
    # Splits text into lines and looks for section headers (e.g., "Experience")
    lines = text.split("\n")
    content = []
    capture = False
    stop_pattern = re.compile(r"|".join(stop_words), re.IGNORECASE)

    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        
        # Start capturing when a keyword is found in a line
        if any(re.search(rf"\b{kw}\b", clean, re.IGNORECASE) for kw in keywords):
            capture = True
            continue

        # Stop capturing when a new section header (stop_word) is detected
        if capture:
            if stop_pattern.search(clean) and len(clean.split()) < 4:
                break
            content.append(clean)

    # Return first 8 lines of the section joined by a separator
    return " | ".join(content[:8])


# ---------------- BATCH PROCESSING ----------------

rows = []

if not TEXT_DIR.exists():
    print(f"❌ Erreur : Le dossier {TEXT_DIR} n'existe pas.")
else:
    for txt_file in TEXT_DIR.glob("*.txt"):
        text = txt_file.read_text(encoding="utf-8", errors="ignore")

        # Map NLP/Regex results to a dictionary
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

# ---------------- CSV EXPORT ----------------

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["cv_id", "name", "email", "phone", "experience", "education", "organizations"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Analyse terminée : {len(rows)} CV extraits → {OUTPUT_FILE}")
