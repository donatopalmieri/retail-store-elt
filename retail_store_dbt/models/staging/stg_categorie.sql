-- models/staging/stg_categorie.sql

SELECT 
    id_categoria,
    nome_categoria,
    descrizione,
    id_categoria_padre
FROM {{ source('staging_raw', 'raw_categorie') }}