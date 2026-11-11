-- models/staging/stg_prodotti.sql

SELECT 
  id_prodotto,
  nome_prodotto,
  categoria,
  prezzo,
  giacenza
FROM {{ source('staging_raw', 'raw_prodotti') }}