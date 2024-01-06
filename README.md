# NHL Data Extract (nhl_api_extract.py)
## Requirements
- you need to provide your own .pem file to interact with the NHL API and put it in the config/ folder. Then update the certificate_file variable in nhl_api_extract.py to match.  

## Generate CSV Extracts
- Run the nhl_api_extract.py and enter values for the desired season and level of detail
- This will produce 3 files: 
  - nhl_players.csv: list of current players for all teams
  - nhl_player_*.csv: stats per player at a season aggregation or an individual game level (gamelog)
  - nhl_teams_*.csv: stats per team for the season selected

## Current Extracts uploaded to Google Sheets
- [Google Sheets](https://docs.google.com/spreadsheets/d/1svydj3EQHsKDweoMvgq188Kh1LqOLdh7ZLkpYeVO7z8/edit?usp=sharing)

## Tableau Dashboards using Data
- [NHL Player Comparator](https://public.tableau.com/app/profile/jesse8369/viz/NHLPlayerComparator/PlayerComparator)
- [NHL Goalie Fantasy Point Scenarios](https://public.tableau.com/app/profile/jesse8369/viz/NHLGoalieComparator/GoalieFantasyPointScenarios)

---  

# NHL Hockey Stats (hockeystats/)

- Portable DuckDB database that uses dbt to combine the output from nhl_api_extract.py and produce reports

---  

# NHL Hockey Stats Output (hockeystats_output/)

- CSV extracts from the dbt project