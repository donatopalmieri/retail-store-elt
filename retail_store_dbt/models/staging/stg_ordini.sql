-- models/staging/stg_ordini.sql

SELECT 
  id_ordine,
  id_cliente,
  data_ordine,
  stato_ordine,
  metodo_pagamento,
  totale_ordine
FROM {{ source('staging_raw', 'raw_ordini') }}