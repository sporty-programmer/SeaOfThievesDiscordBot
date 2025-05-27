# SeaOfThievesDiscordBot
Let your own Discord-Bot show you the stats of your Sea Of Thieves Account

## Required components:
- Raspberry Pi with Internet connection and HTTPS available
- A running Discord-Bot

### 1. Install required Python-Packages:
- dotenv
- redis
- urllib3
- requests
- pandas

> sudo apt install python3-dotenv python3-redis python3-urllib3 python3-requests python3-pandas

### 2. Insert code
- "main.py", "get_api_key.py", "discord_bot" & "data" -> project directory
- <a href="https://github.com/Rapptz/discord.py/archive/refs/heads/master.zip">discord.py.zip</a> -> "discord.py-master/discord" -> project directory

### 3. Configure settings
1. Open the <a href="https://www.seaofthieves.com/de">Sea Of Thieves Website</a> and login.\
2. Now execute "get_api_key.py" to save the API-Key to the cache.\
3. Unfortunately, an  API-Key will only last for 24h and there is no refresh-key, as far as I know.
