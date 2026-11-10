import duckdb
from src.config import DB_PATH

def run_final_analytics():
    con = duckdb.connect(str(DB_PATH))
    
    print("=== VERIFICA TABELLE NEL DWH ===")
    tables = con.execute("SHOW TABLES;").fetchdf()
    print(tables)
    
    print("\n=== REPORT FINALE: Fatturato e volumi per Categoria Prodotto ===")
    query_report = """
        SELECT 
            p.categoria,
            COUNT(f.id_transazione) AS numero_transazioni_totali,
            SUM(f.quantita) AS pezzi_venduti_totali,
            ROUND(SUM(f.fatturato_totale), 2) AS fatturato_complessivo
        FROM fact_vendite f
        JOIN dim_prodotti p ON f.id_prodotto = p.id_prodotto_surrogato
        GROUP BY p.categoria
        ORDER BY fatturato_complessivo DESC;
    """
    df_report = con.execute(query_report).fetchdf()
    print(df_report)
    
    con.close()

if __name__ == "__main__":
    run_final_analytics()