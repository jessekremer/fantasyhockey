{{ 
    config(materialized='table') 
}}

with nhl_teams as (SELECT * FROM {{ ref('nhl_teams_20232024') }})
select * from nhl_teams