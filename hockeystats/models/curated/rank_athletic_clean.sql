{{ 
    config(
        materialized='table'
    )
}}

with 
    rank_athletic as (select * from {{ ref('rank_athletic') }}),

    rank_athletic_clean as (
        select 
            replace(replace(ra.name,'Tim St�tzle','Tim Stützle'),'Alexis Lafreni�re','Alexis Lafrenière') as better_name, 
            ra.*
        from 
            rank_athletic ra
        )

select * from rank_athletic_clean