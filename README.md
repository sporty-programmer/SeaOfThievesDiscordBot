# SeaOfThievesDiscordBot
Let your own Discord-Bot show you the stats of your Sea Of Thieves Account

## Required components:
- Raspberry Pi with Internet connection and HTTPS available
- A running Discord-Bot

### 1. Install the required packages
- python-dotenv
- pandas
- discord.py
- browser_cookie3

### 2. Insert code
- "main.py", "get_api_key.py" & "discord_bot" -> project directory

### 3. Configure settings
1. Open the <a href="https://www.seaofthieves.com/de">Sea Of Thieves Website</a> and login.\
2. Now execute "get_api_key.py" to save the API-Key to the cache.\
3. Unfortunately, an  API-Key will only last for 24h and there is no Refresh-Key, as far as I know, so you need to execute "get_api_key.py" from time to time.
