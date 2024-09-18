{{ 
    config(materialized='table') 
}}

with nhl_stats_current as (select * from {{ ref('nhl_games_singleSeason') }})
select * from nhl_stats