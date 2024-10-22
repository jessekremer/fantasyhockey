{{ 
    config(materialized='table') 
}}

with nhl_teams as (SELECT * FROM {{ ref('nhl_teams') }})
select * from nhl_teams