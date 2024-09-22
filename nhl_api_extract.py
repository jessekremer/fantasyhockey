# New API
# https://www.reddit.com/r/hockey/comments/17qu8by/nhl_api_down_looking_for_alternatives_software/
# https://github.com/Zmalski/NHL-API-Reference

# # Team Stats
# https://api.nhle.com/stats/rest/en/team/summary?sort=shotsForPerGame&cayenneExp=seasonId=20232024%20and%20gameTypeId=2

# # Toronto players
# https://api-web.nhle.com/v1/roster/TOR/current

# # Auston Matthews 20232024 gamelog
# https://api-web.nhle.com/v1/player/8479318/game-log/20232024/2

# # All season level stats by player
# https://api-web.nhle.com/v1/player/8479318/landing
# leagueAbbrev: = "NHL"

# blocks and hits and avgtimeOnIce
# https://api.nhle.com/stats/rest/en/skater/realtime?limit=-1&cayenneExp=seasonId=20232024%20and%20gameTypeId=2


# to get verify=certificate_file to work I had to run the following: pip install pip-system-certs

import requests
from datetime import datetime
import json
import sys

# certificate_file='config/nhle-com.pem' # provide your own

periodType='singleSeason'

team_csv='teamId,period,name,abbreviation,teamName,shortName,gamesPlayed,wins,losses,ot,pts,ptPctg,goalsPerGame,goalsAgainstPerGame,evGGARatio,powerPlayPercentage,powerPlayGoals,powerPlayGoalsAgainst,powerPlayOpportunities,penaltyKillPercentage,shotsPerGame\n'
player_csv='playerId,fullName,firstName,lastName,currentAge,birthDate,rookie,primaryPosition,primaryPositionType,currentTeamId\n'
game_csv='playerId,periodType,period,date,teamId,opponentId,timeOnIce,assists,goals,pim,shots,games,hits,powerPlayGoals,powerPlayPoints,powerPlayTimeOnIce,evenTimeOnIce,penaltyMinutes,faceOffPct,gameWinningGoals,overTimeGoals,shortHandedGoals,shortHandedPoints,shortHandedTimeOnIce,blocked,plusMinus,points,shifts,ot,shutouts,ties,wins,losses,saves,powerPlaySaves,shortHandedSaves,evenSaves,shortHandedShots,evenShots,powerPlayShots,decision,savePercentage,gamesStarted,shotsAgainst,goalsAgainst,powerPlaySavePercentage,evenStrengthSavePercentage,win\n'

# testing values
# seasonId = ['20232024']
# teams = [{'name': 'New York Rangers', 'teamAbbrev': 'NYR'},{'name': 'Dallas Stars', 'teamAbbrev': 'DAL'}]

seasonId = ['20232024','20222023','20212022','20202021','20192020']
teams=[
    {'name': 'New York Rangers', 'teamAbbrev': 'NYR'},
    {'name': 'Dallas Stars', 'teamAbbrev': 'DAL'},
    {'name': 'Carolina Hurricanes', 'teamAbbrev': 'CAR'},
    {'name': 'Winnipeg Jets', 'teamAbbrev': 'WPG'},
    {'name': 'Florida Panthers', 'teamAbbrev': 'FLA'},
    {'name': 'Vancouver Canucks', 'teamAbbrev': 'VAN'},
    {'name': 'Boston Bruins', 'teamAbbrev': 'BOS'},
    {'name': 'Colorado Avalanche', 'teamAbbrev': 'COL'},
    {'name': 'Edmonton Oilers', 'teamAbbrev': 'EDM'},
    {'name': 'Toronto Maple Leafs', 'teamAbbrev': 'TOR'},
    {'name': 'Nashville Predators', 'teamAbbrev': 'NSH'},
    {'name': 'Los Angeles Kings', 'teamAbbrev': 'LAK'},
    {'name': 'Tampa Bay Lightning', 'teamAbbrev': 'TBL'},
    {'name': 'Vegas Golden Knights', 'teamAbbrev': 'VGK'},
    {'name': 'New York Islanders', 'teamAbbrev': 'NYI'},
    {'name': 'St. Louis Blues', 'teamAbbrev': 'STL'},
    {'name': 'Washington Capitals', 'teamAbbrev': 'WSH'},
    {'name': 'Detroit Red Wings', 'teamAbbrev': 'DET'},
    {'name': 'Pittsburgh Penguins', 'teamAbbrev': 'PIT'},
    {'name': 'Minnesota Wild', 'teamAbbrev': 'MIN'},
    {'name': 'Philadelphia Flyers', 'teamAbbrev': 'PHI'},
    {'name': 'Buffalo Sabres', 'teamAbbrev': 'BUF'},
    {'name': 'New Jersey Devils', 'teamAbbrev': 'NJD'},
    {'name': 'Calgary Flames', 'teamAbbrev': 'CGY'},
    {'name': 'Seattle Kraken', 'teamAbbrev': 'SEA'},
    {'name': 'Ottawa Senators', 'teamAbbrev': 'OTT'},
    # {'name': 'Arizona Coyotes', 'teamAbbrev': 'ARI'}, # renamed in 2024
    {'name': 'Utah Hockey Club', 'teamAbbrev': 'UTA'},
    {'name': 'Montréal Canadiens', 'teamAbbrev': 'MTL'},
    {'name': 'Columbus Blue Jackets', 'teamAbbrev': 'CBJ'},
    {'name': 'Anaheim Ducks', 'teamAbbrev': 'ANA'},
    {'name': 'Chicago Blackhawks', 'teamAbbrev': 'CHI'},
    {'name': 'San Jose Sharks', 'teamAbbrev': 'SJS'}
]

def calculate_age(birthdate_str):
    # Convert the string to a datetime object
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    
    # Get today's date
    today = datetime.today().date()
    
    # Calculate age
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


baseURL = 'https://api-web.nhle.com/v1/'
certificate_file='config/nhle-com.pem' # provide your own
teamStandingsAPI='https://api-web.nhle.com/v1/standings/now'
teamStatAPI='https://api.nhle.com/stats/rest/en/team/summary?sort=shotsForPerGame&cayenneExp=seasonId=20232024%20and%20gameTypeId=2'

r = requests.get('https://api.nhle.com/stats/rest/en/team/summary?sort=shotsForPerGame&cayenneExp=seasonId='+str(seasonId[0])+'%20and%20gameTypeId=2', verify=certificate_file)
teamAPI = r.json()
for t in teamAPI['data']:
    team_csv+=str(t['teamId'])+','
    team_csv+=str(seasonId[0])+','
    team_csv+=str(t['teamFullName'])+','
    team_csv+=',,,'
    team_csv+=str(t['gamesPlayed'])+','
    team_csv+=str(t['wins'])+','
    team_csv+=str(t['losses'])+','
    team_csv+=','
    team_csv+=str(t['points'])+','
    team_csv+=str(t['pointPct'])+','
    team_csv+=str(t['goalsForPerGame'])+','
    team_csv+=str(t['goalsAgainstPerGame'])+','
    team_csv+=','
    team_csv+=str(t['powerPlayPct'])+','
    team_csv+=',,,'
    team_csv+=str(t['penaltyKillPct'])+','
    team_csv+=str(t['shotsForPerGame'])
    team_csv+='\n'

for t in teams:
    print('\n'+t['teamAbbrev'])
    r = requests.get(baseURL+'roster/'+t['teamAbbrev']+'/current',verify=certificate_file)
    players = r.json()
    for p in players['forwards']:
        print('f', end='', flush=True)
        player_csv+=str(p['id'])+','
        player_csv+=str(p['firstName']['default']+" "+p['lastName']['default'])+','
        player_csv+=str(p['firstName']['default'])+','
        player_csv+=str(p['lastName']['default'])+','
        player_csv+=str(calculate_age(p['birthDate']))+','
        player_csv+=str(p['birthDate'])+','
        player_csv+=',' #rookie
        player_csv+=str(p['positionCode'])+','
        player_csv+='Forward'+','
        player_csv+=t['teamAbbrev'] #currentTeamId
        player_csv+='\n'
        if periodType=='singleSeason':
            r = requests.get(baseURL+'player/'+str(p['id'])+'/landing',verify=certificate_file)
            singleSeason = r.json()
            for s in singleSeason['seasonTotals']:
                if s['leagueAbbrev'] == 'NHL':
                    game_csv+=str(p['id'])+','
                    game_csv+='singleSeason,'
                    game_csv+=str(s['season'])+','
                    game_csv+=',,,'#date,teamId,opponentId
                    game_csv+=str(s['avgToi'])+',' # convert to seconds from MM:SS format
                    game_csv+=str(s['assists'])+','
                    game_csv+=str(s['goals'])+','
                    game_csv+=str(s['pim'])+','
                    game_csv+=str(s['shots'])+','
                    game_csv+=str(s['gamesPlayed'])+','
                    game_csv+=',' # hits
                    game_csv+=str(s['powerPlayGoals'])+','
                    game_csv+=str(s['powerPlayPoints'])+','
                    game_csv+=',' # powerPlayTimeOnIce
                    game_csv+=',' # evenTimeOnIce
                    game_csv+=',' # penaltyMinutes
                    game_csv+=',' # faceOffPct
                    game_csv+=',' # gameWinningGoals
                    game_csv+=str(s['otGoals'])+','
                    game_csv+=str(s['shorthandedGoals'])+','
                    game_csv+=str(s['shorthandedPoints'])+','
                    game_csv+=',' # shortHandedTimeOnIce
                    game_csv+=',' # blocked
                    game_csv+=str(s['plusMinus'])+','
                    game_csv+=str(s['points'])+','
                    game_csv+=',,,,,,,,,,,,,,,,,,,,'
                    game_csv+='\n'
    for p in players['defensemen']:
        print('d', end='', flush=True)
        player_csv+=str(p['id'])+','
        player_csv+=str(p['firstName']['default']+" "+p['lastName']['default'])+','
        player_csv+=str(p['firstName']['default'])+','
        player_csv+=str(p['lastName']['default'])+','
        player_csv+=str(calculate_age(p['birthDate']))+','
        player_csv+=str(p['birthDate'])+','
        player_csv+=',' #rookie
        player_csv+=str(p['positionCode'])+','
        player_csv+='Defenseman'+','
        player_csv+=t['teamAbbrev'] #currentTeamId
        player_csv+='\n'
        if periodType=='singleSeason':
            r = requests.get(baseURL+'player/'+str(p['id'])+'/landing',verify=certificate_file)
            singleSeason = r.json()
            for s in singleSeason['seasonTotals']:
                if s['leagueAbbrev'] == 'NHL':
                    game_csv+=str(p['id'])+','
                    game_csv+='singleSeason,'
                    game_csv+=str(s['season'])+','
                    game_csv+=',,,'#date,teamId,opponentId
                    game_csv+=str(s['avgToi'])+',' # convert to seconds from MM:SS format
                    game_csv+=str(s['assists'])+','
                    game_csv+=str(s['goals'])+','
                    game_csv+=str(s['pim'])+','
                    game_csv+=str(s['shots'])+','
                    game_csv+=str(s['gamesPlayed'])+','
                    game_csv+=',' # hits
                    game_csv+=str(s['powerPlayGoals'])+','
                    game_csv+=str(s['powerPlayPoints'])+','
                    game_csv+=',' # powerPlayTimeOnIce
                    game_csv+=',' # evenTimeOnIce
                    game_csv+=',' # penaltyMinutes
                    game_csv+=',' # faceOffPct
                    game_csv+=',' # gameWinningGoals
                    game_csv+=str(s['otGoals'])+','
                    game_csv+=str(s['shorthandedGoals'])+','
                    game_csv+=str(s['shorthandedPoints'])+','
                    game_csv+=',' # shortHandedTimeOnIce
                    game_csv+=',' # blocked
                    game_csv+=str(s['plusMinus'])+','
                    game_csv+=str(s['points'])+','
                    game_csv+=',,,,,,,,,,,,,,,,,,,,'
                    game_csv+='\n'

# blocks and hits - to be aggregated in dbt
if periodType=='singleSeason':
    for s in seasonId:
        r = requests.get('https://api.nhle.com/stats/rest/en/skater/realtime?limit=-1&cayenneExp=seasonId='+s+'%20and%20gameTypeId=2',verify=certificate_file)
        singleSeason = r.json()
        print('\n')
        for d in singleSeason['data']:
            print('.', end='', flush=True)
            game_csv+=str(d['playerId'])+','
            game_csv+='singleSeason,'
            game_csv+=s+','
            game_csv+=',' # date
            # game_csv+=str(d['teamAbbrevs'])+','
            game_csv+=',' # team - can be multiple
            game_csv+=',,,,,,,'
            game_csv+=str(d['hits'])+','
            game_csv+=',,,,,,,,,,,'
            game_csv+=str(d['blockedShots'])+','
            game_csv+=',,,,,,,,,,,,,,,,,,,,,,'
            game_csv+='\n'

# game_csv+=player_game_row
with open('hockeystats/seeds/nhl_teams.csv','w',encoding='utf-8') as splits_file:
    splits_file.write(team_csv)
    print('\n[Done] hockeystats/seeds/nhl_teams.csv')

with open('hockeystats/seeds/nhl_players.csv','w',encoding='utf-8') as splits_file:
    splits_file.write(player_csv)
    print('[Done] hockeystats/seeds/nhl_players.csv')

with open('hockeystats/seeds/nhl_games_'+periodType+'.csv','w',encoding='utf-8') as splits_file:
    splits_file.write(game_csv)
    print('[Done] hockeystats/seeds/nhl_games_'+periodType+'.csv')