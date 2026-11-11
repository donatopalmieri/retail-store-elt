-- models/intermediate/int_ordini_dettagli_prodotti.sql

WITH ordini AS (
    SELECT * FROM {{ ref('stg_ordini') }}
),

dettagli AS (
    SELECT * FROM {{ ref('stg_dettaglio_ordini') }}
),

prodotti AS (
    SELECT * FROM {{ ref('stg_prodotti') }}
)

SELECT 
    -- Identificativi
    d.id_dettaglio,
    o.id_ordine,
    o.id_cliente,
    d.id_prodotto,
    
    -- Attributi descrittivi (portati dietro da prodotti)
    p.nome_prodotto,
    
    -- Date e metriche transazionali
    o.data_ordine,
    d.quantita,
    d.prezzo_unitario,
    
    -- Calcolo del fatturato di riga
    (d.quantita * d.prezzo_unitario) AS importo_totale_riga,
    
    o.stato_ordine

FROM dettagli d
INNER JOIN ordini o ON d.id_ordine = o.id_ordine
LEFT JOIN prodotti p ON d.id_prodotto = p.id_prodotto