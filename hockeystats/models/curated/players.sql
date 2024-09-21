{{ 
    config(materialized='table') 
}}

with 
    nhl_players as (select * from {{ ref('nhl_players') }}),
    games as (select * from {{ ref('nhl_games_singleSeason') }}),

    rookie as (
        -- A player must not have played in more than 25 NHL games in any preceding seasons, 
        -- nor in six or more NHL games in each of any two preceding seasons. 
        -- Any player at least 26 years of age (by September 15th of that season) is not considered a rookie.
        select 
            np.playerId,
            case when sum(g.games) <= 25 then 1 else 0 end as total_games,
            case when sum(case when right(g.period,4)::integer = {{ var("current_season") }}-1 then g.games else 0 end) < 6 then 1 else 0 end
            + case when sum(case when right(g.period,4)::integer = {{ var("current_season") }}-2 then g.games else 0 end) < 6 then 1 else 0 end as two_years,
            case when datediff('year',np.birthDate::date,({{ var("current_season") }} -1 || '-09-15')::date) < 26 then 1 else 0 end as age,
            case when total_games+two_years+age = 4 then 'True' else 'False' end as rookieFlag
        from
            nhl_players np
            left outer join games g on g.playerId = np.playerId
        group by
            np.playerId,
            np.birthDate
    ),
    players as (
        select 
            np.*,
            r.rookieFlag
        from 
            nhl_players np
            inner join rookie r on r.playerId = np.playerId
    )
select * from players