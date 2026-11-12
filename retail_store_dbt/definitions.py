import os
from pathlib import Path
from dagster import Definitions, asset
from dagster_dbt import DbtCliResource, dbt_assets

# Percorso alla cartella del progetto dbt (dove si trova dbt_project.yml)
DBT_PROJECT_DIR = Path(__file__).resolve().parent

# Percorso alla cartella dei profili dbt dell'utente (C:\Users\xxxx\.dbt)
PROFILES_DIR = Path.home() / ".dbt"

# 1. ASSET DI INGESTION PYTHON
@asset(
    group_name="ingestion_layer",
    description="Carica i dati grezzi nel database DuckDB."
)
def python_csv_ingestion():
    import duckdb
    db_path = DBT_PROJECT_DIR.parent / "data" / "processed" / "warehouse.duckdb"
    con = duckdb.connect(str(db_path))
    print("=== INGESTION IN ESECUZIONE ===")
    con.close()
    print("=== INGESTION COMPLETATA ===")


# 2. ASSET DBT GENERATI DAL MANIFEST
@dbt_assets(
    manifest=DBT_PROJECT_DIR / "target" / "manifest.json"
)
def ecommerce_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# 3. REGISTRAZIONE DELLE DEFINIZIONI E RISORSE
defs = Definitions(
    assets=[python_csv_ingestion, ecommerce_dbt_assets],
    resources={
        "dbt": DbtCliResource(
            project_dir=os.fspath(DBT_PROJECT_DIR),
            profiles_dir=os.fspath(PROFILES_DIR),
        ),
    },
)