{{ 
    config(materialized='table') 
}}

with
    player_stats as (select * from {{ ref('player_stats') }}),
    players as (select * from {{ ref('players') }}),
    teams as (select * from {{ ref('teams') }}),

    current_season as (select 2025 as period),
    stats as (
        select 
            p.playerId,
            p.firstName,
            p.lastName,
            concat(concat(p.firstName, ' '), p.lastName) as fullName,
            p.primaryPosition,
            t.abbreviation as team,
            p.currentAge,
            p.currentAge-(cs.period-right(ps.period,4)::integer) as age,
            ps.period,
            ps.timeOnIce,
            ps.games,
            ps.games/82 as health_pct,
            ps.goals,			-- 3
            ps.assists,			-- 2
            ps.pim, 			-- 0.5
            ps.powerPlayPoints,	-- 2
            ps.shortHandedGoals,-- 2
            ps.shortHandedPoints,-- 1
            ps.gameWinningGoals,-- 2
            ps.shots, 			-- 0.5
            ps.hits,			-- 0.2
            ps.blocked,			-- 1
            ps.goals*3
            +ps.assists*2
            +ps.pim*-0.5
            +ps.powerPlayPoints*2
            +ps.shortHandedGoals*2
            +ps.shortHandedPoints*1
            +ps.gameWinningGoals*2
            +ps.shots*0.5
            +ps.hits*0.2
            +ps.blocked*1 as fpts
        from 
            players p
            inner join player_stats ps on ps.playerId = p.playerId
            left outer join teams t on t.teamId = p.currentTeamId and t.period = ps.period 
            inner join current_season cs on 1=1
        where 
            p.rookie = 'False'
        and p.primaryPosition <> 'G'),
    avg_health as (
        select 
            stats.playerId,
            round(avg(health_pct),2) pct
        from
            stats
        group by 
            stats.playerId),
    history as (
        select 
            stats.playerId,
            stats.firstName,
            stats.lastName,
            stats.fullName,
            stats.primaryPosition,
            stats.team,
            stats.currentAge,
            stats.age,
            stats.period,
            stats.timeOnIce,
            stats.games,
            stats.health_pct,
            stats.goals,
            stats.assists,
            stats.pim,
            stats.powerPlayPoints,
            stats.shortHandedGoals,
            stats.shortHandedPoints,
            stats.gameWinningGoals,
            stats.shots,
            stats.hits,
            stats.blocked,
            stats.fpts,
            case when ah.pct > 0.5 then round(stats.fpts*(82/games),1) else stats.fpts end as fpts_82,
            ah.pct as health_modifier,
            case 
                when stats.age < 24 then 1.2
                when stats.age < 27 then 1.02
                when stats.age < 30 then 0.93
                when stats.age < 33 then 0.94
                when stats.age < 36 then 1.07
                when stats.age < 39 then 1.1	
            else 1 end as age_modifier,
            case 
                when stats.currentAge < 24 then 1.2
                when stats.currentAge < 27 then 1.02
                when stats.currentAge < 30 then 0.93
                when stats.currentAge < 33 then 0.94
                when stats.currentAge < 36 then 1.07
                when stats.currentAge < 39 then 1.1	
            else 1 end as current_age_modifier	 
        from
            stats
            inner join avg_health ah on ah.playerId = stats.playerId)

select * from history