-- models/staging/stg_clienti.sql

SELECT 
    id_cliente,
    nome,
    cognome,
    email,
    citta,
    data_registrazione
FROM {{ source('staging_raw', 'raw_clienti') }}