import sqlite3
import pandas as pd
from pathlib import Path

# Paths for database and training data
DB_PATH = Path("../../backend/cv_extractions.db")
DATA_DIR = Path("../data/training")
DATA_DIR.mkdir(exist_ok=True, parents=True)

def prepare_training_set():
    # 1. Connect to the SQLite database
    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # 2. Query only the CVs validated by humans
    # We use the 'corrected' fields as the new target labels (Ground Truth)
    query = """
    SELECT 
        raw_text, 
        corrected_name, 
        corrected_email, 
        corrected_phone, 
        corrected_orgs, 
        corrected_experience, 
        corrected_education
    FROM extractions 
    WHERE status = 'validated'
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("⚠️ No validated data found. Keep annotating!")
        return

    # 3. Save the dataset for the retraining process
    output_path = DATA_DIR / "ground_truth_dataset.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    
    print(f"✅ Training set prepared: {len(df)} samples saved to {output_path}")

if __name__ == "__main__":
    prepare_training_set()