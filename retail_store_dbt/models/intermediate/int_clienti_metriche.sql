-- models/intermediate/int_clienti_metriche.sql

WITH clienti AS (
    SELECT * FROM {{ ref('stg_clienti') }}
),

ordini_dettagli AS (
    SELECT * FROM {{ ref('int_ordini_dettagli_prodotti') }}
),

metriche_per_cliente AS (
    SELECT
        id_cliente,
        COUNT(DISTINCT id_ordine) AS numero_ordini_totali,
        SUM(importo_totale_riga) AS spesa_totale_cliente,
        MIN(data_ordine) AS data_primo_ordine,
        MAX(data_ordine) AS data_ultimo_ordine
    FROM ordini_dettagli
    GROUP BY id_cliente
)

SELECT
    c.id_cliente,
    c.nome,
    c.cognome,
    c.email,
    
    -- Gestione dei valori nulli per chi non ha mai ordinato (0 o default)
    COALESCE(m.numero_ordini_totali, 0) AS numero_ordini_totali,
    COALESCE(m.spesa_totale_cliente, 0) AS spesa_totale_cliente,
    
    m.data_primo_ordine,
    m.data_ultimo_ordine

FROM clienti c
LEFT JOIN metriche_per_cliente m ON c.id_cliente = m.id_cliente