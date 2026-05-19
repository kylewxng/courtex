from nba_api.stats.endpoints import LeagueGameLog, PlayByPlayV3
import time
import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd


df = LeagueGameLog(season="2024-25").get_data_frames()[0]
game_ids = df['GAME_ID'].unique()

dfs = []
for game_id in game_ids[:200]:
    try:
        game = PlayByPlayV3(game_id=game_id).get_data_frames()[0]
        game = game[game['actionType'].isin(['Made Shot', 'Missed Shot'])]
        game = game[['gameId', 'actionNumber', 'description', 'actionType', 'clock', 'xLegacy', 'yLegacy']]
        game.rename(columns={'gameId': 'game_id', 'actionNumber':'event_num', 'actionType':'action_type', 'xLegacy':'x_legacy', 'yLegacy':'y_legacy'}, inplace=True)
        dfs.append(game)
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.6)

print(f"Pulled {len(dfs)} games")
print(dfs[0].head())
print(dfs[0].columns)

# Set up Supabase client
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

client = create_client(url, key)
print("Supabase client created successfully:", client)

# Ingest data into Supabase
dfs_concat = pd.concat(dfs).drop_duplicates(subset=['game_id', 'event_num'])
dfs = dfs_concat.to_dict(orient='records')

for i in range(0, len(dfs), 500):
    batch = dfs[i:i+500]
    client.table("plays").upsert(batch, on_conflict="game_id,event_num").execute()