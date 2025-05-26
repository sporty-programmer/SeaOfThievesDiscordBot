from requests import Session, Response, JSONDecodeError

from pandas import DataFrame


class APIrate:

    """
    Opens (and holds open) a session for Sea Of Thieves data-retrieval.
    """

    def __init__(self, api_key: str) -> None:

        """
        Creates a session for API-calls.
        :param api_key: API-Key (user-specific)
        """

        headers: dict[str, str] = {'Referer': 'https://www.seaofthieves.com/'}
        cookies: dict[str, str] = {'rat': api_key}

        self._session: Session = Session()
        self._session.headers.update(headers)
        self._session.cookies.update(cookies)


    def stop(self) -> None:

        """
        Closes session.
        :return:
        """

        self._session.close()


    def get_actions(self) -> dict:

        """
        Returns a dict with all possible API-calls.
        :return: dict with callables
        """

        return {
            "reputation": lambda: self.reputation,
            "balance": lambda: self.balance,
            "captaincy": lambda: self.captaincy,
            "chest": lambda: self.chest,
            "achievements": lambda: self.achievements,
            "overview": lambda: self.overview
        }


    @property
    def reputation(self) -> str:

        """
        Returns information about the user's reputation.
        :return:
        """

        response: dict = self._get_response("reputation")
        data_lines: list[tuple[str, str]] = []
        for name in response.keys():
            if not "Level" in response[name]:
                continue
            data_lines.append((f"{name}:", response[name]["Level"]))
        answer: str = DataFrame(data=data_lines, columns=("Fraction:", "Level")).to_string(index=False)
        return answer


    @property
    def balance(self) -> str:

        """
        Returns information about the user's balance.
        :return:
        """

        response: dict = self._get_response("balance")
        wanted: tuple[str, ...] = ("title", "ancientCoins", "doubloons", "gold")
        data_lines: list[tuple[str, str]] = []
        for name in wanted:
            data_lines.append((f"{name.capitalize()}:", response[name]))
        answer: str = DataFrame(data=data_lines, columns=("Currency:", "Amount")).to_string(index=False)
        return answer


    @property
    def captaincy(self) -> str:

        """
        Returns information about the user's balance.
        :return:
        """

        response: dict = self._get_response("captaincy")
        answer: str = "Not implemented yet."
        return answer


    @property
    def chest(self) -> str:

        """
        Returns information about the user's chest.
        :return:
        """

        response: dict = self._get_response("chest")
        answer: str = "Not implemented yet."
        return answer


    @property
    def achievements(self) -> str:

        """
        Returns information about the user's achievements.
        :return:
        """

        response: dict = self._get_response("achievements")
        answer: str = "Not implemented yet."
        return answer


    @property
    def overview(self) -> str:

        """
        Returns information about the user's overview.
        :return:
        """

        response: dict = self._get_response("overview")
        answer: str = "Not implemented yet."
        return answer


    def _get_response(self, topic: str) -> dict:

        """
        Sends a request to the Sea Of Thieves API and returns the response.
        :param topic: what kind of information should get received
        :return: if possible JSON decoded response, else empty dict
        """

        url: str = f"https://www.seaofthieves.com/api/profilev2/{topic}"

        response: Response = self._session.get(url)

        if response.status_code == 404:
            return {}

        try:
            return response.json()

        except JSONDecodeError:
            return {}