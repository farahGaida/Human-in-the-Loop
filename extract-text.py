import pdfplumber
from pathlib import Path

# Define input and output dir
input_dir = Path("data/raw_cvs")
output_dir = Path("data/text")

# Create the output folder if it doesn't exist
output_dir.mkdir(exist_ok=True)

for pdf_path in input_dir.glob("*.pdf"):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    txt_path = output_dir / (pdf_path.stem + ".txt")
    txt_path.write_text(text, encoding="utf-8")

print("✅ Extraction terminée")
