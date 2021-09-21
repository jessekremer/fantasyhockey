#Uses the NHL api to pull data on all current players for each of the teams

#https://hackernoon.com/retrieving-hockey-stats-from-the-nhls-undocumented-api-zz3003wrw
#https://nhl-api.surge.sh/?ref=hackernoon.com

#individual games example
#https://statsapi.web.nhl.com/api/v1/people/8480800/stats?stats=gameLog&season=20202021
#full season for player
#https://statsapi.web.nhl.com/api/v1/people/8471679/stats?stats=statsSingleSeason&season=20202021
#teams something example
#https://statsapi.web.nhl.com/api/v1/teams/3/stats?stats=gameLog&season=20202021

# PP opportunities
#https://statsapi.web.nhl.com/api/v1/game/2020020177/feed/live?site=en_nhl

import requests
import json
import sys

#how many rows to return from each api call
limit = 200
game_header='playerId,periodType,period,date,teamId,opponentId,timeOnIce,assists,goals,pim,shots,games,hits,powerPlayGoals,powerPlayPoints,powerPlayTimeOnIce,evenTimeOnIce,penaltyMinutes,faceOffPct,gameWinningGoals,overTimeGoals,shortHandedGoals,shortHandedPoints,shortHandedTimeOnIce,blocked,plusMinus,points,shifts,ot,shutouts,ties,wins,losses,saves,powerPlaySaves,shortHandedSaves,evenSaves,shortHandedShots,evenShots,powerPlayShots,decision,savePercentage,gamesStarted,shotsAgainst,goalsAgainst,powerPlaySavePercentage,evenStrengthSavePercentage,win\n'
game_csv=game_header

print("\n[What NHL Data?]")
print("1 = Everything (teams + players)")
print("2 = Teams only\n")
what_data=input("Choice (1 or 2)? ")
if not what_data:
    what_data='1'
print(what_data)
print("\n[What Season]")
print("example: 20202021\n")
season=input("What Season? ")
if not season:
    season='20202021'
    print("Defaulted to: 20202021")
if what_data=='1':
    print("[What Level of Detail?\n")
    print("1 = Season Total")
    print("2 = Individual Games\n")
    lod=input("Choice (1 or 2)? ")
    if lod=='1':
        periodType='singleSeason'
    elif lod=='2':
        periodType='gamelog'
    else:
        periodType='singleSeason'
player_game_row=''
team_csv='teamId,period,name,abbreviation,teamName,shortName,gamesPlayed,wins,losses,ot,pts,ptPctg,goalsPerGame,goalsAgainstPerGame,evGGARatio,powerPlayPercentage,powerPlayGoals,powerPlayGoalsAgainst,powerPlayOpportunities,penaltyKillPercentage,shotsPerGame,shotsAllowed,winScoreFirst,winOppScoreFirst,winLeadFirstPer,winLeadSecondPer,winOutshootOpp,winOutshotByOpp,faceOffsTaken,faceOffsWon,faceOffsLost,faceOffWinPercentage,shootingPctg,savePctg,wins_rank,losses_rank,ot_rank,pts_rank,ptPctg_rank,goalsPerGame_rank,goalsAgainstPerGame_rank,evGGARatio_rank,powerPlayPercentage_rank,powerPlayGoals_rank,powerPlayGoalsAgainst_rank,powerPlayOpportunities_rank,penaltyKillPercentage_rank,shotsPerGame_rank,shotsAllowed_rank,winScoreFirst_rank,winOppScoreFirst_rank,winLeadFirstPer_rank,winLeadSecondPer_rank,winOutshootOpp_rank,winOutshotByOpp_rank,faceOffsTaken_rank,faceOffsWon_rank,faceOffsLost_rank,faceOffWinPercentage_rank,shootingPctg_rank,savePctg_rank\n'
player_csv='playerId,fullName,firstName,lastName,currentAge,rookie,primaryPosition,primaryPositionType,currentTeamId\n'

baseurl='https://statsapi.web.nhl.com'
r = requests.get(baseurl+'/api/v1/teams')
teams = r.json()      
# print(baseurl+'/api/v1/teams')
for t in teams['teams']:
    team_csv+=str(t['id'])
    team_csv+=','+season+','
    team_csv+=t['name']
    team_csv+=','
    team_csv+=t['abbreviation']
    team_csv+=','
    team_csv+=t['teamName']
    team_csv+=','
    if 'shortname' in t:
        team_csv+=t['shortName']
    team_csv+=','
    # get team stats
    tr = requests.get(baseurl+'/api/v1/teams/'+str(t['id'])+'/stats?season='+season)
    teams_stats=tr.json()
    try:
        ts=teams_stats['stats'][0]['splits'][0]['stat']    
        team_csv+=str(ts['gamesPlayed'])
        team_csv+=','
        team_csv+=str(ts['wins'])
        team_csv+=','
        team_csv+=str(ts['losses'])
        team_csv+=','
        team_csv+=str(ts['ot'])
        team_csv+=','
        team_csv+=str(ts['pts'])
        team_csv+=','
        team_csv+=str(ts['ptPctg'])
        team_csv+=','
        team_csv+=str(ts['goalsPerGame'])
        team_csv+=','
        team_csv+=str(ts['goalsAgainstPerGame'])
        team_csv+=','
        team_csv+=str(ts['evGGARatio'])
        team_csv+=','
        team_csv+=str(ts['powerPlayPercentage'])
        team_csv+=','
        team_csv+=str(ts['powerPlayGoals'])
        team_csv+=','
        team_csv+=str(ts['powerPlayGoalsAgainst'])
        team_csv+=','
        team_csv+=str(ts['powerPlayOpportunities'])
        team_csv+=','
        team_csv+=str(ts['penaltyKillPercentage'])
        team_csv+=','
        team_csv+=str(ts['shotsPerGame'])
        team_csv+=','
        team_csv+=str(ts['shotsAllowed'])
        team_csv+=','
        team_csv+=str(ts['winScoreFirst'])
        team_csv+=','
        team_csv+=str(ts['winOppScoreFirst'])
        team_csv+=','
        team_csv+=str(ts['winLeadFirstPer'])
        team_csv+=','
        team_csv+=str(ts['winLeadSecondPer'])
        team_csv+=','
        team_csv+=str(ts['winOutshootOpp'])
        team_csv+=','
        team_csv+=str(ts['winOutshotByOpp'])
        team_csv+=','
        team_csv+=str(ts['faceOffsTaken'])
        team_csv+=','
        team_csv+=str(ts['faceOffsWon'])
        team_csv+=','
        team_csv+=str(ts['faceOffsLost'])
        team_csv+=','
        team_csv+=str(ts['faceOffWinPercentage'])
        team_csv+=','
        team_csv+=str(ts['shootingPctg'])
        team_csv+=','
        team_csv+=str(ts['savePctg'])
        team_csv+=','
    except:
        print('No stats for '+t['name'])
    # team stat ranks
    try:
        ts=teams_stats['stats'][1]['splits'][0]['stat']
        team_csv+=ts['wins']
        team_csv+=','
        team_csv+=ts['losses']
        team_csv+=','
        team_csv+=ts['ot']
        team_csv+=','
        team_csv+=ts['pts']
        team_csv+=','
        team_csv+=ts['ptPctg']
        team_csv+=','
        team_csv+=ts['goalsPerGame']
        team_csv+=','
        team_csv+=ts['goalsAgainstPerGame']
        team_csv+=','
        team_csv+=ts['evGGARatio']
        team_csv+=','
        team_csv+=ts['powerPlayPercentage']
        team_csv+=','
        team_csv+=ts['powerPlayGoals']
        team_csv+=','
        team_csv+=ts['powerPlayGoalsAgainst']
        team_csv+=','
        team_csv+=ts['powerPlayOpportunities']
        team_csv+=','
        team_csv+=ts['penaltyKillPercentage']
        team_csv+=','
        team_csv+=ts['shotsPerGame']
        team_csv+=','
        team_csv+=ts['shotsAllowed']
        team_csv+=','
        team_csv+=ts['winScoreFirst']
        team_csv+=','
        team_csv+=ts['winOppScoreFirst']
        team_csv+=','
        team_csv+=ts['winLeadFirstPer']
        team_csv+=','
        team_csv+=ts['winLeadSecondPer']
        team_csv+=','
        team_csv+=ts['winOutshootOpp']
        team_csv+=','
        team_csv+=ts['winOutshotByOpp']
        team_csv+=','
        team_csv+=ts['faceOffsTaken']
        team_csv+=','
        team_csv+=ts['faceOffsWon']
        team_csv+=','
        team_csv+=ts['faceOffsLost']
        team_csv+=','
        team_csv+=ts['faceOffWinPercentage']
        team_csv+=','
        team_csv+=ts['shootingPctRank']
        team_csv+=','
        team_csv+=ts['savePctRank']
    except:
        print('No stats ranks for '+t['name'])
    team_csv+='\n'
    if what_data=='1':
        teamplayerapi = t['link']+'/roster'
        r= requests.get(baseurl+teamplayerapi)
        team_players = r.json()
        for p in team_players['roster']:
            #print(baseurl+teamplayerapi)
            playerapi=p['person']['link']
            r = requests.get(baseurl+playerapi)    
            player = r.json()
            player_csv+=str(player['people'][0]['id'])
            player_csv+=','
            player_csv+=player['people'][0]['fullName']
            player_csv+=','
            player_csv+=player['people'][0]['firstName']
            player_csv+=','
            player_csv+=player['people'][0]['lastName']
            player_csv+=','
            player_csv+=str(player['people'][0]['currentAge'])
            player_csv+=','
            player_csv+=str(player['people'][0]['rookie'])
            player_csv+=','
            player_csv+=player['people'][0]['primaryPosition']['code']
            player_csv+=','
            player_csv+=player['people'][0]['primaryPosition']['type']
            player_csv+=','
            player_csv+=str(t['id'])
            player_csv+='\n'
            #print(baseurl+playerapi)
            if periodType=='gamelog':
                periodapi='/stats?stats=gameLog&season='+season
            else:
                periodapi='/stats?stats=statsSingleSeason&season='+season
            r = requests.get(baseurl+playerapi+periodapi)
            games = r.json()
            # print(baseurl+playerapi+periodapi)
            for ig in games['stats'][0]['splits']:
            #for ig in g['splits']:
                player_game_row+=str(player['people'][0]['id'])+','
                player_game_row+=periodType+','
                player_game_row+=season+','
                if 'date' in ig:
                    player_game_row+=ig['date']
                player_game_row+=','
                if 'team' in ig:
                    if 'id' in ig['team']:
                        player_game_row+=str(ig['team']['id'])
                    else:
                        player_game_row+=str(t['id'])#use currentTeamId if pulling season stats
                player_game_row+=','
                if 'opponent' in ig:
                    if 'id' in ig['opponent']:
                        player_game_row+=str(ig['opponent']['id'])
                player_game_row+=','
                if 'timeOnIce' in ig['stat']:
                    #player_game_row+=ig['stat']['timeOnIce']
                    time=ig['stat']['timeOnIce']
                    player_game_row+=str(round(int(time[0:time.find(':')])+int(time[time.find(':')+1:])/60,2))
                player_game_row+=','
                if 'assists' in ig['stat']:
                    player_game_row+=str(ig['stat']['assists'])
                player_game_row+=','
                if 'goals' in ig['stat']:
                    player_game_row+=str(ig['stat']['goals'])
                player_game_row+=','
                if 'pim' in ig['stat']:
                    player_game_row+=str(ig['stat']['pim'])
                player_game_row+=','
                if 'shots' in ig['stat']:
                    player_game_row+=str(ig['stat']['shots'])
                player_game_row+=','
                if 'games' in ig['stat']:
                    player_game_row+=str(ig['stat']['games'])
                player_game_row+=','
                if 'hits' in ig['stat']:
                    player_game_row+=str(ig['stat']['hits'])
                player_game_row+=','
                if 'powerPlayGoals' in ig['stat']:
                    player_game_row+=str(ig['stat']['powerPlayGoals'])
                player_game_row+=','
                if 'powerPlayPoints' in ig['stat']:
                    player_game_row+=str(ig['stat']['powerPlayPoints'])
                player_game_row+=','
                if 'powerPlayTimeOnIce' in ig['stat']:
                    time=ig['stat']['powerPlayTimeOnIce']
                    player_game_row+=str(round(int(time[0:time.find(':')])+int(time[time.find(':')+1:])/60,2))
                player_game_row+=','
                if 'evenTimeOnIce' in ig['stat']:
                    time=ig['stat']['evenTimeOnIce']
                    player_game_row+=str(round(int(time[0:time.find(':')])+int(time[time.find(':')+1:])/60,2))
                player_game_row+=','
                if 'penaltyMinutes' in ig['stat']:
                    player_game_row+=str(ig['stat']['penaltyMinutes'])
                player_game_row+=','
                if 'faceOffPct' in ig['stat']:
                    player_game_row+=str(ig['stat']['faceOffPct'])
                player_game_row+=','
                if 'gameWinningGoals' in ig['stat']:
                    player_game_row+=str(ig['stat']['gameWinningGoals'])
                player_game_row+=','
                if 'overTimeGoals' in ig['stat']:
                    player_game_row+=str(ig['stat']['overTimeGoals'])
                player_game_row+=','
                if 'shortHandedGoals' in ig['stat']:
                    player_game_row+=str(ig['stat']['shortHandedGoals'])
                player_game_row+=','
                if 'shortHandedPoints' in ig['stat']:
                    player_game_row+=str(ig['stat']['shortHandedPoints'])
                player_game_row+=','
                if 'shortHandedTimeOnIce' in ig['stat']:
                    time=ig['stat']['shortHandedTimeOnIce']
                    player_game_row+=str(round(int(time[0:time.find(':')])+int(time[time.find(':')+1:])/60,2))
                player_game_row+=','
                if 'blocked' in ig['stat']:
                    player_game_row+=str(ig['stat']['blocked'])
                player_game_row+=','
                if 'plusMinus' in ig['stat']:
                    player_game_row+=str(ig['stat']['plusMinus'])
                player_game_row+=','
                if 'points' in ig['stat']:
                    player_game_row+=str(ig['stat']['points'])
                player_game_row+=','
                if 'shifts' in ig['stat']:
                    player_game_row+=str(ig['stat']['shifts'])
                player_game_row+=','
                #goalie
                if 'ot' in ig['stat']:
                    player_game_row+=str(ig['stat']['ot'])
                player_game_row+=','
                if 'shutouts' in ig['stat']:
                    player_game_row+=str(ig['stat']['shutouts'])
                player_game_row+=','
                if 'ties' in ig['stat']:
                    player_game_row+=str(ig['stat']['ties'])
                player_game_row+=','
                if 'wins' in ig['stat']:
                    player_game_row+=str(ig['stat']['wins'])
                player_game_row+=','
                if 'losses' in ig['stat']:
                    player_game_row+=str(ig['stat']['losses'])
                player_game_row+=','
                if 'saves' in ig['stat']:
                    player_game_row+=str(ig['stat']['saves'])
                player_game_row+=','
                if 'powerPlaySaves' in ig['stat']:
                    player_game_row+=str(ig['stat']['powerPlaySaves'])
                player_game_row+=','
                if 'shortHandedSaves' in ig['stat']:
                    player_game_row+=str(ig['stat']['shortHandedSaves'])
                player_game_row+=','
                if 'evenSaves' in ig['stat']:
                    player_game_row+=str(ig['stat']['evenSaves'])
                player_game_row+=','
                if 'shortHandedShots' in ig['stat']:
                    player_game_row+=str(ig['stat']['shortHandedShots'])
                player_game_row+=','
                if 'evenShots' in ig['stat']:
                    player_game_row+=str(ig['stat']['evenShots'])
                player_game_row+=','
                if 'powerPlayShots' in ig['stat']:
                    player_game_row+=str(ig['stat']['powerPlayShots'])
                player_game_row+=','
                if 'decision' in ig['stat']:
                    player_game_row+=str(ig['stat']['decision'])
                player_game_row+=','
                if 'savePercentage' in ig['stat']:
                    player_game_row+=str(ig['stat']['savePercentage'])
                player_game_row+=','
                if 'gamesStarted' in ig['stat']:
                    player_game_row+=str(ig['stat']['gamesStarted'])
                player_game_row+=','
                if 'shotsAgainst' in ig['stat']:
                    player_game_row+=str(ig['stat']['shotsAgainst'])
                player_game_row+=','
                if 'goalsAgainst' in ig['stat']:
                    player_game_row+=str(ig['stat']['goalsAgainst'])
                player_game_row+=','
                if 'powerPlaySavePercentage' in ig['stat']:
                    player_game_row+=str(ig['stat']['powerPlaySavePercentage'])
                player_game_row+=','
                if 'evenStrengthSavePercentage' in ig['stat']:
                    player_game_row+=str(ig['stat']['evenStrengthSavePercentage'])
                player_game_row+=','
                if 'isWin' in ig:
                    player_game_row+=str(ig['isWin'])
                    # if str(ig['isWin']) == 'TRUE':
                        # player_game_row+='win'
                    # else:
                        # player_game_row+='loss'
                player_game_row+='\n'
    print(t['name']+' done')
    
game_csv+=player_game_row
splits_file = open('nhl_teams_'+season+'.csv','w')
splits_file.write(team_csv)
splits_file.close()
if what_data=='1':
    splits_file = open('nhl_players.csv','w')
    splits_file.write(player_csv)
    splits_file.close()
    splits_file = open('nhl_player_'+season+'_'+periodType+'.csv','w')
    splits_file.write(game_csv)
    splits_file.close()
