from typing import Callable

from discord.ext.commands import Author

from .sea_of_thieves_api import APIrate

from .api_key_manager import APIKeyManager


class Responder:

    """
    Delivers responses for the Discord-Bot.
    """

    def __init__(self, cache_path: str) -> None:

        """
        Initializes API backends for each user listed in cache.
        :param cache_path: path to cache file (absolute path recommended)
        """

        self._cache_path: str = cache_path

        self._api_key_manager: APIKeyManager = APIKeyManager(cache_path=cache_path)

        self._apirates: dict[str, APIrate] = {user_name: APIrate(api_key) for user_name, api_key in self._api_key_manager.get().items()}


    def get_responses(self, author: Author, keywords: list[str]) -> list[str]:

        """
        Returns response for author and message.
        :param author: author of message
        :param keywords: part of message that should get read and responded
        :return: response
        """

        responses: list[str] = []

        apirate, actions = self._get_apirate(author.name) # get apirate and possible ways for data retrieval for user

        for keyword in keywords:

            # check for new api-key
            if self._handle_new_api_key(keyword, author.name, responses):
                apirate, actions = self._get_apirate(author.name)  # get new apirate and new possible ways for data retrieval for user in cause of new key

            # next iteration if no apirate because of missing permission for data retrieval with api
            if not apirate:
                continue

            # next iteration if api data retrieval successful because keyword handled
            if self._handle_api_call(keyword, actions, responses):
                continue

        return responses


    def _get_apirate(self, user_name: str) -> tuple[APIrate | None, dict[str, Callable]]:

        """
        Returns APIrate object and actions dict for user (if possible).
        :param user_name: Discord name of user
        :return: tuple with APIrate object and dict with all callables for data retrieval
        """

        apirate: APIrate | None = self._apirates.get(user_name, None) # apirate from user

        actions: dict[str, Callable] = apirate.get_actions() if apirate else {} # actions for user

        return apirate, actions


    def _handle_new_api_key(self, keyword: str, user_name: str, responses: list[str]) -> bool:

        """
        Checks if new API-Key given and saves new API-Key to API-Key-Manager.
        :param user_name: Discord name of user
        :param keyword: keyword to scan
        :param responses: list in which the Discord response should be saved
        :return: True if new key set, else False
        """

        if keyword.startswith("api_key="):

            api_key_new = keyword.split("=", 1)[1]  # extract api-key

            self._api_key_manager.update(user_name=user_name, api_key_new=api_key_new)  # add new api-key to manager

            self._apirates[user_name] = APIrate(api_key=api_key_new)  # add new apirate to list

            responses.append(f"API-Key set to: {api_key_new}")

            return True # if new api-key found

        return False # if no new api-key found


    def _handle_api_call(self, keyword: str, actions: dict[str, Callable], responses: list[str]) -> bool: # NOQA

        """
        Handles API-call and adds response to given list.
        :param keyword: keyword to handle
        :param actions: dict with possible actions for different keyword
        :param responses: list in which the response should be saved
        :return: True if keyword handled, False if keyword not found in actions dict
        """

        for key, action in actions.items():

            # next iteration if key not requested
            if key != keyword:
                continue

            action_response: str = action() # receive response

            # next iteration if response empty
            if not action_response:
                continue

            responses.append(action_response) # append action response to responses list

            return True # if keyword handled

        return False # if keyword not handled