import sys

from os import path, chdir

import signal

from time import sleep as delay

from dotenv import dotenv_values

from discord_bot import Bot, BotHandler


# PREPARATIONS
chdir(cwd := path.dirname(path.realpath(__file__))) # set cwd


# LOAD SETTINGS
discord_bot_token: str = dotenv_values(f"{cwd}/data/discord/.env")["BOT_TOKEN"]
sot_cache_path: str = f"{cwd}/data/sea_of_thieves/.cache"
bot_listening_mark: str = "!"


# INITIALIZE BOT

bot: Bot = Bot(
    cache_path=sot_cache_path
)

bot_handler: BotHandler = BotHandler(
    bot=bot,
    token=discord_bot_token
)

bot_handler.start()


# PREPARE EXIT

def clean_up(signum: int, frame) -> None: # NOQA
    global bot_handler
    bot_handler.stop()
    print("Bot stopped gently.")
    sys.exit(0)

signal.signal(signal.SIGTERM, clean_up)
signal.signal(signal.SIGINT, clean_up)


# MAIN-LOOP
while True:
    delay(0.1)