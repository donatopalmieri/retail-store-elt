
# 🛍️ Retail Store Data Warehouse (ELT & DuckDB)

Un progetto di **Data Engineering end-to-end** che implementa una pipeline **ELT (Extract, Load, Transform)** leggera ma robusta, sviluppata in **Python** e basata su **DuckDB**. Il data model segue i principi della modellazione dimensionale di **Kimball** (Schema a Stella / Star Schema).

---

## 🏗️ Architettura del Progetto

Il progetto separa nettamente i dati grezzi da quelli elaborati seguendo i layer tipici del Modern Data Stack:
1. **Raw Layer (`data/raw/`)**: Contiene i file di origine (es. CSV grezzi di clienti e vendite) senza alcuna manipolazione.
2. **Staging Layer**: Specchio fedele dei dati grezzi caricati nel database analitico.
3. **Data Warehouse Layer (`data/processed/warehouse.duckdb`)**: Contiene le tabelle dimensionali (`dim_clienti`, `dim_prodotti`) e la tabella dei fatti (`fact_vendite`), arricchite con regole di **Data Quality** e collegate tramite chiavi surrogate.

# 📂 Struttura delle Cartelle

```text
retail_store/
├── data/
│   ├── raw/                 # File sorgente grezzi (CSV)
│   └── processed/           # Database DuckDB consolidato (warehouse.duckdb)
├── src/
│   ├── config.py            # Gestione centralizzata dei percorsi
│   ├── ingestion/           # Script di caricamento (Raw -> Staging)
│   ├── transformations/     # Script di pulizia e popolamento DWH
│   └── analytics/           # Script di reportistica e metriche di business
├── requirements.txt         # Dipendenze Python
└── README.md

# Guida all'Uso e Installazione

1. Clonare il repository e configurare l'ambiente virtuale
Bash
# Clona il repository o apri la cartella del progetto
cd retail_store

# Crea e attiva l'ambiente virtuale (consigliato)
python -m venv venv
# Su Windows:
venv\Scripts\activate
# Su Mac/Linux:
source venv/bin/activate
2. Installare le dipendenze
Bash
pip install -r requirements.txt
(Assicurati di avere almeno duckdb e pandas installati).

3. Eseguire la Pipeline ELT
Esegui gli script in sequenza dalla root del progetto:

Step 1: Ingestion (Caricamento dei dati grezzi)

Bash
python -m src.ingestion.load_csv_clienti
python -m src.ingestion.load_csv_vendite
Step 2: Trasformazione e Data Quality (Popolamento DWH)

Bash
python -m src.transformations.staging_to_dwh
Step 3: Reportistica e Verifica Finale

Bash
python -m src.analytics.report_vendite