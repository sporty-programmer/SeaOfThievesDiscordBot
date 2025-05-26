class APIKeyManager:

    """
    Manages API-Keys for Sea Of Thieves data-retrieval with help of a cache file.
    """

    def __init__(self, cache_path: str) -> None:

        """
        Automatically loads API-Keys from cache.
        :param cache_path: path to cache file (absolute path recommended)
        """

        self._cache_path: str = cache_path

        self._api_keys: dict[str, str] = self.get()


    def get_user(self, user_name: str) -> str:

        """
        Returns to API-Key of a specific user.
        :param user_name: user's Discord name
        :return: user's API-Key
        """

        return self._api_keys[user_name]


    def get(self) -> dict[str, str]:

        """
        Returns a dict with every API-Key
        :return: dict with API-Keys
        """

        api_keys: dict[str, str] = {}

        with open(self._cache_path, "r") as file:

            lines: list[str] = file.read().split("\n")

        for line in lines:

            if not "=" in line:
                continue

            user_name, api_key = line.split("=", 1)

            api_keys[user_name] = api_key

        return api_keys


    def set(self, api_keys_new: dict[str, str], auto_save: bool = True) -> None:

        """
        Replaces old API-Keys dict with a new one.
        :param api_keys_new: dict with usernames and API-Keys
        :param auto_save: whether the new dict should be saved automatically to cache
        :return:
        """

        self._api_keys = api_keys_new

        if auto_save:
            self.save()


    def update(self, user_name: str, api_key_new: str, auto_save: bool = True) -> None:

        """
        Adds or changes an API-Key of a specific user.
        :param user_name: Discord name
        :param api_key_new: API-Key
        :param auto_save: whether the new dict should be saved automatically to cache
        :return:
        """

        self._api_keys[user_name] = api_key_new

        if auto_save:
            self.save()


    def save(self) -> None:

        """
        Saves current API-Keys to cache.
        :return:
        """

        with open(self._cache_path, "w") as file:

            for user_name, api_key in self._api_keys.items():

                file.write(f"{user_name}={api_key}")