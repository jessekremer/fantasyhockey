{{ 
    config(materialized='table') 
}}

with
    games as (select * from {{ ref('games') }}),
    players as (select * from {{ ref('players') }}),
    teams as (select * from {{ ref('teams') }}),

    stats as (
        select 
            p.playerId,
            p.firstName,
            p.lastName,
            concat(concat(p.firstName, ' '), p.lastName) as fullName,
            p.primaryPosition,
            p.currentTeamId as team,
            p.currentAge,
            p.currentAge as age,
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
            inner join games ps on ps.playerId = p.playerId
        where 
            p.rookieFlag = 'False'
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