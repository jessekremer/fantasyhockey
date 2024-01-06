{{ 
    config(materialized='table') 
}}

with nhl_players as (SELECT * FROM {{ ref('nhl_players') }})
select * from nhl_players