from discord import Intents, Client, Message
from discord.errors import LoginFailure

from .chat_protocols import Responder


class Bot(Client):

    """
    Discord-Bot which is able to deliver information about Sea Of Thieves (and the user)
    """

    def __init__(self, cache_path: str, listening_mark: str = "!") -> None:

        """
        Initializes the bot.
        :param cache_path: path to cache file for Sea Of Thieves API-Keys (absolute path recommended)
        """

        self._cache_path: str = cache_path
        self._listening_mark: str = listening_mark

        intents: Intents = Intents.default()
        intents.message_content = True  # NOQA

        super().__init__(intents=intents)

        self._responder: Responder = Responder(cache_path=cache_path) # delivers responses for received messages


    async def login(self, token: str) -> None:

        try:
            await super().login(token)
            print("Token accepted.")

        except LoginFailure as e:
            print(f"LoginFailure: {e}")


    async def on_ready(self) -> None:
        print(f"\"{self.user}\" is now online.")


    async def on_error(self, event: str, *args, **kwargs) -> None:
        print(f"Error occurred at {event} -> {args} & {kwargs}")


    async def on_message(self, message: Message) -> None:

        # abort if message is from bot itself
        if message.author == self.user:
            return

        # abort if bot does not get requested to listen
        if not message.content.startswith(self._listening_mark):
            return

        keywords: list[str] = message.content.split(sep=" ")

        responses: list[str] = self._responder.get_responses(author=message.author, keywords=keywords)

        # abort if no response found
        if not responses:
            return

        response: str = "\n\n".join(responses)

        heading_line: str = f"@{message.author.global_name} (@{message.author.name})"

        full_response: str = f"{heading_line}\n```{response}```"

        await message.channel.send(full_response)