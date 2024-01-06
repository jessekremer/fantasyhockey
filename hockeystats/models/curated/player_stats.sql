{{ 
    config(materialized='table') 
}}

with 
    nhl_stats_current as (select * from {{ ref('nhl_player_20232024_singleSeason') }}),
    nhl_stats_1yago as (select * from {{ ref('nhl_player_20222023_singleSeason') }}),
    nhl_stats_2yago as (select * from {{ ref('nhl_player_20212022_singleSeason') }}),
    nhl_stats_3yago as (select * from {{ ref('nhl_player_20202021_singleSeason') }}),

    nhl_stats as (
        select * from nhl_stats_1yago
        union all
        select * from nhl_stats_2yago
        union all
        select * from nhl_stats_3yago
    )

select * from nhl_stats