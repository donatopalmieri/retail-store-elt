from pathlib import Path

# Trova la cartella principale del progetto (la root) partendo da dove si trova questo file
BASE_DIR = Path(__file__).resolve().parent.parent

# Definiamo i percorsi principali
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Spostiamo il database dentro la cartella processed/
DB_PATH = PROCESSED_DIR / "warehouse.duckdb"

print(f"Directory radice del progetto: {BASE_DIR}")