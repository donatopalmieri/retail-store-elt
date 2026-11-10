import duckdb
from src.config import DB_PATH

def run_dwh_transformations():
    print("=== AVVIO TRASFORMAZIONI DWH (Staging -> DWH) ===")
    
    con = duckdb.connect(str(DB_PATH))
    
    # 1. Creazione della Dimensione Clienti (rimuovendo eventuali duplicati con DISTINCT o GROUP BY)
    con.execute("""
        CREATE OR REPLACE TABLE dim_clienti AS
        SELECT DISTINCT
            ROW_NUMBER() OVER () AS id_cliente_surrogato,
            id_cliente, -- ID originale dal gestionale/file
            nomecliente,
            citta,
            segmento
        FROM stg_clienti
        WHERE id_cliente IS NOT NULL;
    """)
    print("-> Tabella 'dim_clienti' creata con successo.")

    # 2. Creazione della Dimensione Prodotti (estratta univocamente dalle vendite o da un catalogo)
    con.execute("""
        CREATE OR REPLACE TABLE dim_prodotti AS
        SELECT DISTINCT
            ROW_NUMBER() OVER () AS id_prodotto_surrogato,
            prodotto AS nome_prodotto,
            categoria
        FROM stg_vendite
        WHERE prodotto IS NOT NULL;
    """)
    print("-> Tabella 'dim_prodotti' creata con successo.")

    # 3. Creazione della Tabella dei Fatti (Fact Vendite) collegando le dimensioni
    con.execute("""
        CREATE OR REPLACE TABLE fact_vendite AS
        SELECT 
            v.id_transazione,
            c.id_cliente_surrogato AS id_cliente,
            p.id_prodotto_surrogato AS id_prodotto,
            v.data,
            coalesce(v.quantita,1) as quantita,
            v.prezzo_unitario,
            (coalesce(v.quantita,1) * v.prezzo_unitario) AS fatturato_totale
        FROM stg_vendite v
        LEFT JOIN dim_clienti c ON v.id_cliente = c.id_cliente
        LEFT JOIN dim_prodotti p ON v.prodotto = p.nome_prodotto;
    """)
    print("-> Tabella 'fact_vendite' creata con successo!")
    
    # Verifichiamo il risultato stampando un'anteprima dei fatti
    preview = con.execute("SELECT * FROM fact_vendite LIMIT 5").fetchdf()
    print("\nAnteprima dati Fact Vendite:")
    print(preview)
    
    con.close()
    print("=== TRASFORMAZIONI DWH COMPLETATE ===")

if __name__ == "__main__":
    run_dwh_transformations()