-- https://theathletic.com/4815363/2023/09/18/fantasy-hockey-cheat-sheet-2023-24/

{{ 
    config(materialized='table') 
}}

with
    player_history as (select * from {{ ref('player_history') }}),
    rank_athletic_cte as (select * from {{ ref('rank_athletic_clean')}}),
    current_season as (select 2024 as period),
    norog as (
        select 
            curr.firstName, 
            curr.lastName, 
            curr.fullName,
            curr.primaryPosition,
            curr.team,
            round(ph_1yago.fpts,1) as fpts_2023,
            round(ph_2yago.fpts,1) as fpts_2022,
            round(ph_3yago.fpts,1) as fpts_2021,
            round(ph_4yago.fpts,1) as fpts_2020,
            -- last year worth 8
            -- 2yago worth 5
            -- 3yago worth 3
            -- 4yago worth 1
            -- current age modifier + health_modifier (based on last 4 years) / 2 
            round(case when 
            (case when ph_1yago.fpts is not null then 8 else 0 end +
            case when ph_2yago.fpts is not null then 5 else 0 end +
            case when ph_3yago.fpts is not null then 3 else 0 end +
            case when ph_4yago.fpts is not null then 1 else 0 end) <> 0 then
            round((case when ph_1yago.fpts is not null then ph_1yago.fpts*8 else 0 end +
            case when ph_2yago.fpts is not null then ph_2yago.fpts*5 else 0 end +
            case when ph_3yago.fpts is not null then ph_3yago.fpts*3 else 0 end +
            case when ph_4yago.fpts is not null then ph_4yago.fpts*1 else 0 end)
            /
            (case when ph_1yago.fpts is not null then 8 else 0 end +
            case when ph_2yago.fpts is not null then 5 else 0 end +
            case when ph_3yago.fpts is not null then 3 else 0 end +
            case when ph_4yago.fpts is not null then 1 else 0 end),1) else 0 end
            *(curr.current_age_modifier+curr.health_modifier)/2,1) as est_fpts
        from 
            player_history curr
            inner join current_season on 1=1
            left outer join player_history ph_1yago on right(ph_1yago.period,4)::integer = current_season.period-1 and curr.playerId = ph_1yago.playerId 
            left outer join player_history ph_2yago on right(ph_2yago.period,4)::integer = current_season.period-2 and curr.playerId = ph_2yago.playerId
            left outer join player_history ph_3yago on right(ph_3yago.period,4)::integer = current_season.period-3 and curr.playerId = ph_3yago.playerId
            left outer join player_history ph_4yago on right(ph_4yago.period,4)::integer = current_season.period-4 and curr.playerId = ph_4yago.playerId
        where 
            right(curr.period,4)::integer = current_season.period-1),
    injuries as (
        -- https://www.cbssports.com/nhl/injuries/
        select 'Isac Lundestrom' as fullName, 'Feb 9' as estimated_return union
        select 'Jack Quinn' as fullName, 'Oct 29' as estimated_return union
        select 'Calum Ritchie' as fullName, 'Nov 1' as estimated_return union
        select 'Chris Wagner' as fullName, 'Feb 5' as estimated_return union
        select 'Gabriel Landeskog' as fullName, 'Apr 1' as estimated_return union
        select 'Brandon Montour' as fullName, 'Dec 12' as estimated_return union
        select 'Aaron Ekblad' as fullName, 'Dec 14' as estimated_return union
        select 'Christian Dvorak' as fullName, 'Nov 2' as estimated_return union
        select 'Ryan Ellis' as fullName, 'Jul 1' as estimated_return union
        select 'Jake Guentzel' as fullName, 'Oct 24' as estimated_return union
        select 'Max Pacioretty' as fullName, 'Nov 2' as estimated_return
    ),
    all_ranks as (
        select 
            nr.firstName, 
            nr.lastName, 
            nr.primaryPosition,
            nr.team,
            case when i.fullName is not null then i.estimated_return else null end as injured,
            nr.est_fpts,
            rank() over (order by nr.est_fpts desc) as norog_rank,
            rank() over (partition by nr.primaryPosition order by nr.est_fpts desc) as norog_pos_rank,
            rank() over (partition by nr.primaryPosition order by ar."POS RK" desc) as athletic_pos_rank,
            ar.RK as athletic_rank,
            ar.POS as athletic_pos
        from
            norog nr
            left outer join rank_athletic_cte ar on ar.better_name = nr.fullName
            left outer join injuries i on i.fullName = nr.fullName)
select 
	ar.firstName, 
	ar.lastName, 
	ar.primaryPosition,
	coalesce(ar.athletic_pos,ar.primaryPosition) as position,
	ar.team,
	ar.injured,
	ar.est_fpts as fpts,
	rank() over (order by (ar.norog_rank*5 + coalesce(ar.athletic_rank,0))/(5+case when ar.athletic_rank is null then 1 else 0 end)) as rnk,
	rank() over (partition by ar.primaryPosition order by (ar.norog_pos_rank*5 + coalesce(ar.athletic_pos_rank,0))/(5+case when ar.athletic_pos_rank is null then 1 else 0 end)) as pos_rnk
from
	all_ranks ar
order by 
	8
