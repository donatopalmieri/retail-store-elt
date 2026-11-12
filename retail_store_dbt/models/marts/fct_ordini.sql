-- models/marts/fct_ordini.sql

{{
    config(
        materialized = 'table'
    )
}}

WITH int_ordini AS (
    SELECT * FROM {{ ref('int_ordini_dettagli_prodotti') }}
),

-- (Facoltativo ma consigliato) Assicuriamoci che esistano nelle dimensioni per mantenere l'integrità
dim_clienti AS (
    SELECT id_cliente FROM {{ ref('dim_clienti') }}
),

dim_prodotti AS (
    SELECT id_prodotto FROM {{ ref('dim_prodotti') }}
)

SELECT
    -- Identificativi univoci della riga di fatto
    o.id_dettaglio,
    o.id_ordine,
    
    -- Chiavi esterne (Foreign Keys verso le dimensioni)
    o.id_cliente,
    o.id_prodotto,
    
    -- Metriche temporali e descrittive
    o.data_ordine,
    o.stato_ordine,
    
    -- Misure / Metriche quantitative
    o.quantita,
    o.prezzo_unitario,
    o.importo_totale_riga

FROM int_ordini o
-- Inner join o Left join a seconda di come vuoi gestire eventuali prodotti/clienti mancanti
INNER JOIN dim_clienti c ON o.id_cliente = c.id_cliente
INNER JOIN dim_prodotti p ON o.id_prodotto = p.id_prodotto