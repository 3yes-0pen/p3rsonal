import requests
import pandas as pd

search_url = "https://api.rawg.io/api/games"
api_key = "bfeb857cb2014f27baf036dc8dda34b9"
def fetch(game_title):
    try:
        search_parameters = {"search": game_title, "key": api_key}
        
        response = requests.get(search_url, search_parameters)

        if response.status_code == 200:
            data = response.json()
            if data["count"] > 0:
                game_id = data["results"][0]["id"]

                details_url = f"https://api.rawg.io/api/games/{game_id}"
                details_parameters = {"key": api_key}
                details_response = requests.get(details_url, params=details_parameters)
                if details_response.status_code == 200:
                    print("Details acquireddd")
                    details_data = details_response.json()
                    game_summary = details_data["description"]
                    metacritic = details_data["metacritic"]
                    return game_summary, metacritic
                else:
                    print(f"Error fetching details the game: {game_title}")
            else:
                print(f"No results found this game: {game_title}")
        else:
            print(f"Error even fetching game: {game_title}")
    except Exception as e:
            print(f"Error processing game: {game_title}. Error: {e}")
            return None 
    
vgoutput = pd.read_csv('~/Python/input/VGoutput.csv')
for index, row in vgoutput.iterrows():
    if index >= 209:
        break
    vg_title = row['name']
    vg_result = fetch(vg_title)
    if vg_result is not None:  # Check if the result is not None
        vg_info, vg_metacritic = vg_result  # Unpack the result
        if 'description' not in vgoutput.columns:
            vgoutput['description'] = None
        if 'metacritic' not in vgoutput.columns:
            vgoutput['metacritic'] = None
        vgoutput.loc[index, 'description'] = vg_info
        vgoutput.loc[index, 'metacritic'] = vg_metacritic
    else:
        print(f"Skipping {vg_title} due to missing data")
print(vgoutput.head(4))
vgoutput.to_csv('~/Python/input/updatedVGOutput.csv', index=False)