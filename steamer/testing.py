import requests
import json

def save_games_list(api_key):
    # Steam Store API endpoint
    api_url = f'https://api.steampowered.com/IStoreService/GetAppList/v1/?key={api_key}&max_results=50000'

    # Make a request to the Steam Store API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Save the games list to a JSON file
        with open("games_list.json", "w") as file:
            json.dump(data, file)
    else:
        print("Error: Unable to retrieve games list.")

def get_app_id(app_name, games_list):
    # Iterate through the list of apps
    for app in games_list['response']['apps']:
        # Check if the app name matches the provided name (case-sensitive)
        if app_name == app['name']:
            # Return the appid if found
            return app['appid']

    # If the app is not found
    return None

def get_game_prices(appid, regions):
    # Print the appid for debugging purposes
    print(f"AppID: {appid}")

    # Iterate through regions and fetch prices
    for region in regions:
        # Make a request to the Steam API for each region
        response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={appid}&cc={region}&l=english&v=1&filters=price_overview')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the game is free to play
            if str(appid) in data and 'success' in data[str(appid)] and data[str(appid)]['success']:
                if not data[str(appid)]['data']:
                    print(f"Region: {region}, Game is free to play")
                else:
                    # Extract and print prices if available
                    price_info = data[str(appid)]['data']['price_overview']
                    currency = price_info['currency']
                    final_price = price_info['final_formatted']
                    print(f"Region: {region}, Price: {final_price} {currency}")
            else:
                print(f"No price information available for region '{region}'")

        else:
            # If the request was not successful
            print(f"Error: Unable to retrieve price data for region '{region}' (Status Code: {response.status_code})")

    # Generate and print the Steam store link
    print(f"Steam Store Link: https://store.steampowered.com/app/{appid}")

if __name__ == "__main__":
    # Check if games list exists
    try:
        with open("games_list.json", "r") as file:
            games_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Games list file doesn't exist or is corrupted, download it
        api_key = input("Enter your Steam API key: ")
        save_games_list(api_key)
        with open("games_list.json", "r") as file:
            games_list = json.load(file)

    # Prompt user for input
    user_input = input("Enter the name of the game: ")

    # Call the function to get appid
    appid = get_app_id(user_input, games_list)

    # Check if appid is found
    if appid:
        # List of regions
        regions = ['TR', 'EU', 'US', 'UK', 'RU', 'UA']

        # Call the function to print appid, get prices, and generate store link for each region
        get_game_prices(appid, regions)
    else:
        print("Game not found.")