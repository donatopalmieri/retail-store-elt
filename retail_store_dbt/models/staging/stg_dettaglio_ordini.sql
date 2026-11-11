-- models/staging/stg_dettaglio_ordini.sql

SELECT 
    id_dettaglio,
    id_ordine,
    id_prodotto,
    quantita,
    prezzo_unitario,
    sconto_percentuale,
    subtotale
FROM {{ source('staging_raw', 'raw_dettaglio_ordini') }}