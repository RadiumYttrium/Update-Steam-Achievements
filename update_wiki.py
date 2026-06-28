import requests
import mwclient
import json
import os
import datetime

bot_username = os.environ.get('WIKI_BOT_USERNAME')
bot_password = os.environ.get('WIKI_BOT_PASSWORD')
steam_api_key = os.environ.get('STEAM_API_KEY')

if not bot_username or not bot_password or not steam_api_key:
    raise ValueError("Missing wiki credentials or Steam API key in environment variables!")

schema_url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={steam_api_key}&appid=1374490"
schema_req = requests.get(schema_url)
schema_data = schema_req.json()

clean_data = {}
if 'game' in schema_data and 'availableGameStats' in schema_data['game']:
    for ach in schema_data['game']['availableGameStats'].get('achievements', []):
        clean_data[ach['name']] = 0.0

percent_url = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=1374490&format=json"
percent_req = requests.get(percent_url)
percent_data = percent_req.json()

for ach in percent_data['achievementpercentages']['achievements']:
    if ach['name'] in clean_data:
        clean_data[ach['name']] = round(float(ach['percent']), 1)

site = mwclient.Site('dragonwilds.runescape.wiki', path='/')
site.login(bot_username, bot_password)

page = site.pages['Module:FetchSteamAchievements/data.json']
page_content = json.dumps(clean_data, indent=4)

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
dynamic_summary = f"Automated update of Steam achievement stats on {current_date}"

if page.text() != page_content:
    page.edit(page_content, summary=dynamic_summary)
    print(dynamic_summary)
else:
    print("No changes detected. Skipping edit.")
