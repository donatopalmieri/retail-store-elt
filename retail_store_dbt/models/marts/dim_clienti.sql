with raw_clienti as (
    select * from {{ source('staging_raw', 'stg_clienti') }}
)

select
    id_cliente,
    trim(Nome) as nome,
    trim(cognome) as cognome,
    lower(trim(email)) as email,
    cast(data_registrazione as date) as data_registrazione
from raw_clienti
where id_cliente is not null