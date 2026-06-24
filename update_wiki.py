import requests
import mwclient
import json
import os
import datetime

url = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=1374490&format=json"
steam_req = requests.get(url)
steam_data = steam_req.json()

clean_data = {}
for ach in steam_data['achievementpercentages']['achievements']:
    clean_data[ach['name']] = round(float(ach['percent']), 1)

site = mwclient.Site('dragonwilds.runescape.wiki', path='/')

bot_username = os.environ.get('WIKI_BOT_USERNAME')
bot_password = os.environ.get('WIKI_BOT_PASSWORD')

if not bot_username or not bot_password:
    raise ValueError("Missing wiki credentials in environment variables!")

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
