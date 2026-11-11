import duckdb
import pandas as pd
from src.config import RAW_DIR, DB_PATH

def run_ingestion_data():
    print("Avvio processo di ingestion completo...\n")
    
    # 1. Definizione del dizionario con tutti i file e le relative tabelle di staging
    tabelle_da_caricare = {
        "clienti": "clienti.csv",
        "categorie": "categorie.csv",
        "prodotti": "prodotti.csv",
        "ordini": "ordini.csv",
        "dettaglio_ordini": "dettaglio_ordini.csv",
        "eventi_web": "eventi_web.csv",
        "resi": "resi.csv"
    }
    
    # 2. Connessione unica a DuckDB
    con = duckdb.connect(str(DB_PATH))
    
    successi = 0
    errori = 0
    
    # 3. Iterazione su tutte le tabelle
    for nome_chiave, nome_file in tabelle_da_caricare.items():
        csv_file = RAW_DIR / nome_file
        table_name = f"stg_{nome_chiave}"
        
        # Controllo di sicurezza se il file esiste
        if not csv_file.exists():
            print(f"[ATTENZIONE] Il file {nome_file} non è stato trovato in {RAW_DIR}. Saltato.")
            errori += 1
            continue
            
        try:
            print(f"Elaborazione in corso: {nome_file} -> {table_name}")
            
            # Leggiamo il CSV con Pandas
            df = pd.read_csv(csv_file)
            
            # Pulizia di base dei nomi delle colonne (es. "Nome Cliente" -> "nome_cliente")
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            
            # Creazione della tabella di Staging in DuckDB partendo dal DataFrame
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            
            # Verifichiamo quante righe sono state caricate
            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"-> Tabella '{table_name}' creata con successo ({count} righe).\n")
            successi += 1
            
        except Exception as e:
            print(f"[ERRORE] Errore durante l'elaborazione di {nome_file}: {e}\n")
            errori += 1

    # Chiusura connessione
    con.close()
    
    print("--------------------------------------------------")
    print(f"Ingestion completata! Tabelle caricate: {successi}, Errori/Saltate: {errori}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_ingestion_data()