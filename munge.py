# place your code to clean up the data file below.
#I used a JupyterLab notebook to code the webscraping portion to create the raw data csv called nba_games.csv
import pandas as pd

df = pd.read_csv('nba_games.csv')
columns = df.columns
for i in columns:
    print(i)

impt_cols = ['team', 'team_opp', 'fga', 'fg%', '3p', '3p%', 'ft', 
             'fta', 'ft%', 'trb', 'ast', 'stl', 'blk', 'tov', 
             'pf', 'pts', 'ortg', 'drtg', 'season', 'won']

df_2023 = df[df['season'] == 2023]
cleaned_df = df_2023[impt_cols].copy()
cleaned_df.to_csv('cleaned_csv')