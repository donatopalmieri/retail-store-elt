import duckdb
from src.config import DB_PATH

def run_exploratory_queries():
    con = duckdb.connect(str(DB_PATH))
    
    print("=== 1. Controllo clienti senza email o con campi vuoti ===")
    df_clienti_anomali = con.execute("""
        SELECT * 
        FROM stg_clienti 
        where Citta is null
    """).fetchdf()
    print(f"Trovati {len(df_clienti_anomali)} clienti con dati mancanti:")
    print(df_clienti_anomali if not df_clienti_anomali.empty else "Nessuna anomalia trovata.")

    print("\n=== 2. Controllo vendite con quantità anomale (es. <= 0) ===")
    df_vendite_anomale = con.execute("""
        SELECT * 
        FROM stg_vendite 
        WHERE quantita IS NULL OR quantita <= 0
    """).fetchdf()
    print(f"Trovate {len(df_vendite_anomale)} vendite con quantità non valide:")
    print(df_vendite_anomale if not df_vendite_anomale.empty else "Nessuna anomalia trovata.")

    print("\n=== 3. Top 5 prodotti per quantità totale venduta ===")
    df_top_prodotti = con.execute("""
        SELECT 
            prodotto, 
            SUM(quantita) AS quantita_totale,
            COUNT(*) AS numero_transazioni
        FROM stg_vendite
        GROUP BY prodotto
        ORDER BY quantita_totale DESC
        LIMIT 5;
    """).fetchdf()
    print(df_top_prodotti)

    con.close()

if __name__ == "__main__":
    run_exploratory_queries()