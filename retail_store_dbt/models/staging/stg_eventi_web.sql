-- models/staging/stg_eventi_web.sql

SELECT 
    id_evento,
    session_id,
    id_cliente,
    tipo_evento,
    id_prodotto,
    url_pagina,
    timestamp
FROM {{ source('staging_raw', 'raw_eventi_web') }}