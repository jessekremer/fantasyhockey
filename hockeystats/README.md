NHL Fantasy hockey stat dbt project
# NHL Hockey Stats dbt-duckdb

## Requirements

- dbt-duckdb


## Set Up

- Run ../nhl_api_extract.py in the pre-season and put the relevant season's data as CSV into hockeystats/seeds
- Visit [The Athletic and use their Excel tool](https://theathletic.com/4815363/2023/09/18/fantasy-hockey-cheat-sheet-2023-24/) with your league's scoring system. Export the rankings to a CSV also in seeds with the name "rank_athletic.csv"
- Optional: adjust the scoring in the stats CTE of models/serving/player_history.sql to match your league's settingsß


## Running the dbt project

- from a terminal in the hockeystats directory:
`dbt build`


## Export to CSV

- from a terminal in the hockeystats directory:  

`duckdb hockeystats.duckdb`  
`copy (select * from draft_ranks) to '../hockeystats_output/NoRoG_Draft_Ranks_20232024.csv' (FORMAT CSV, HEADER);`

- Now the CSV will be in ../hockeystats_ouput.