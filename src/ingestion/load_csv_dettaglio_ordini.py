import duckdb
import pandas as pd
from src.config import RAW_DIR, DB_PATH

def run_ingestion_dettaglio_ordini():
    print("Avvio processo di ingestion...")
    
    # Esempio: supponiamo di avere un file chiamato 'vendite.csv' in data/raw/
    csv_file = RAW_DIR / "dettaglio_ordini.csv"
    
    # Controllo di sicurezza se il file esiste
    if not csv_file.exists():
        print(f"Attenzione: Il file {csv_file.name} non è stato trovato in {RAW_DIR}.")
        print("Metti un file CSV di prova lì dentro per testare lo script.")
        return

    # 1. Leggiamo il CSV con Pandas
    print(f"Lettura del file: {csv_file.name}")
    df = pd.read_csv(csv_file)
    
    # 2. Pulizia di base dei nomi delle colonne (es. "Nome Cliente" -> "nome_cliente")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # 3. Connessione a DuckDB (se il file warehouse.duckdb non esiste, viene creato ora)
    con = duckdb.connect(str(DB_PATH))
    
    # 4. Creazione della tabella di Staging in DuckDB partendo dal DataFrame di Pandas
    table_name = "stg_dettaglio_ordini"
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    
    print(f"Tabella '{table_name}' creata con successo in DuckDB!")
    
    # Verifichiamo quante righe sono state caricate
    count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Righe caricate nella staging: {count}")
    
    # Chiusura connessione
    con.close()

if __name__ == "__main__":
    run_ingestion_dettaglio_ordini()