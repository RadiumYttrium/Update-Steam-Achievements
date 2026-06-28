This repository automates the process of pulling live global completion percentages for Steam achievements and syncing them directly to the RuneScape: Dragonwilds Wiki. This uses the Steam Web API and pushes a formatted JSON dictionary using mwclient (from MediaWiki).

**Endpoints**
* ***GetSchemaForGame***: Gethes the master list of all programmed achievements for API ID 1374490 (''RuneScape: Dragonwilds'').
* ***GetGlobalAchievementPercentagesForApp***: Fetches live completion achievement percentages.

This formats all percentages to a float and pushes the resulting to Module:FetchSteamAchivements/data.json on the wiki.

**Automated Schedule**
This pipeline is automated via (.github/workflows/update_steam.yml)

* Runs every 12 hours (in UTC) via cron.
* Can be triggered via Workflow Dispatch.
* Bypasses edits if the live Steam data has not changed since the last run to prevent revision history clutter.

Variables
| Secret Name | Description |
| :--- | :--- |
| **STEAM_API_KEY** | A valid Steam Web API key to access the game schema endpoint. |
| **WIKI_BOT_USERNAME** | The Bot Username generated via `Special:BotPasswords` on the wiki. |
| **WIKI_BOT_PASSWORD** | The secure token generated for the bot account. |
