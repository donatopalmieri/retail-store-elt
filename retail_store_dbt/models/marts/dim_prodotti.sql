-- models/marts/dim_prodotti.sql

{{
    config(
        materialized = 'table'
    )
}}

WITH prodotti AS (
    SELECT * FROM {{ ref('stg_prodotti') }}
),

categorie AS (
    SELECT * FROM {{ ref('stg_categorie') }}
)

SELECT
    -- Chiave primaria della dimensione
    p.id_prodotto,
    
    -- Attributi descrittivi del prodotto
    p.nome_prodotto,
    p.prezzo,
    
    -- Informazioni di categoria (denormalizzate per comodità di analisi)
    p.categoria,
    c.nome_categoria,
    c.descrizione

FROM prodotti p
LEFT JOIN categorie c ON p.categoria = c.nome_categoria