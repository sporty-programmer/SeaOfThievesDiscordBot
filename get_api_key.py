from sys import exit as sys_exit

from os import path, chdir, makedirs

import browser_cookie3

from requests.utils import dict_from_cookiejar

from http.cookiejar import CookieJar

import webbrowser

from discord_bot import APIKeyManager


# PREPARATIONS

# set current working directory
chdir(cwd := path.dirname(path.realpath(__file__)))

# set paths
base_dir: str = f"{cwd}/data/sea_of_thieves"
sot_cache_path: str = f"{base_dir}/.cache"

# create dir if necessary
if not path.exists(sot_cache_path):

    makedirs(base_dir, exist_ok=True)

    with open(sot_cache_path, "w") as file:
        pass


# LOGIN REQUEST

print("Please make sure to be logged in on https://www.seaofthieves.com/de and to use Firefox.\n")

webbrowser.open("https://www.seaofthieves.com/de")

while True:
    match input("Logged in? [y/n] "):
        case "y":
            break
        case "n":
            sys_exit(0)
        case _:
            pass


# GATHER COOKIES

cookie_jar: CookieJar = browser_cookie3.firefox() # gather all cookies

cookie_dict: dict[str, str] = dict_from_cookiejar(cookie_jar) # convert cookies to dict

api_key: str = cookie_dict.get("rat", "") # try to retrieve cookie named "rat"

user_name: str = input("Discord name: ")

api_key_manager: APIKeyManager = APIKeyManager(sot_cache_path) # initialize api-key-manager

api_key_manager.update(user_name, api_key) # add new key to cache


# inform user
print("\nAPI-Key found and saved in API-Key-Manager." if api_key else "No API-Key found.")


# hold window open
input("\nPress ENTER to close this window.")