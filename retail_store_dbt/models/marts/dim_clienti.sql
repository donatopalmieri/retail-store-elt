-- models/marts/dim_clienti.sql

{{
    config(
        materialized = 'table'
    )
}}

WITH clienti_metriche AS (
    SELECT * FROM {{ ref('int_clienti_metriche') }}
)

SELECT
    -- Chiave primaria della dimensione
    id_cliente,
    
    -- Attributi anagrafici
    nome,
    cognome,
    email,
    
    -- Metriche di performance del cliente
    numero_ordini_totali,
    spesa_totale_cliente,
    data_primo_ordine,
    data_ultimo_ordine,
    
    -- Esempio di logica di business / Segmentazione cliente
    CASE 
        WHEN numero_ordini_totali = 0 THEN 'Non attivo'
        WHEN spesa_totale_cliente >= 500 THEN 'VIP'
        WHEN numero_ordini_totali > 1 THEN 'Fedele'
        ELSE 'Nuovo / Singolo Acquisto'
    END AS segmento_cliente

FROM clienti_metriche