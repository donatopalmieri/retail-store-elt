-- models/staging/stg_resi.sql

SELECT 
  id_reso,
  id_dettaglio_ordine,
  data_reso,
  quantita_resa,
  motivo_reso,
  stato_reso,
  importo_rimborso
FROM {{ source('staging_raw', 'raw_resi') }}