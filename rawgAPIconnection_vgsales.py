import requests
import pandas as pd


VGsales = pd.read_csv('~/Python/input/vgsales.csv')
dropped_cols = ['Rank', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
VGsales = VGsales.drop(columns=dropped_cols)

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
    
for index, row in VGsales.iterrows():
    if index >= 2000:
        break 
    game_title = row['Name']
    game_result = fetch(game_title)
    if game_result is not None:
        game_info, metacritic = game_result
        if 'description' not in VGsales.columns:
            VGsales['description'] = None
        if 'metacritic' not in VGsales.columns:
            VGsales['metacritic'] = None
        VGsales.loc[index, 'description'] = game_info
        VGsales.loc[index, 'metacritic'] = metacritic
    else:
        print(f"Skipping {game_title} due to missing data")

print(VGsales.head(4))
VGsales.to_csv('~/Python/input/updatedVGSales.csv', index=False)