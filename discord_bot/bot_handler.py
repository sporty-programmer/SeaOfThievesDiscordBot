from threading import Thread, Event

from asyncio import new_event_loop, set_event_loop, create_task
from asyncio import AbstractEventLoop

from time import sleep as delay

from discord_bot import Bot


class BotHandler:

    def __init__(self, bot: Bot, token: str) -> None:

        self._bot: Bot = bot
        self._token: str = token

        self._loop: AbstractEventLoop = new_event_loop()

        set_event_loop(self._loop)

        self._loop.create_task(bot.start(token=token))

        self._thread: Thread = Thread(
            target=self._loop.run_forever,
            daemon=True
        )


    def start(self) -> None:

        self._thread.start()


    def stop(self) -> None:

        done: Event = Event()

        async def wrapper() -> None:
            await self._bot.close()
            self._loop.stop()
            done.set()

        self._loop.call_soon_threadsafe(create_task, wrapper())

        # wait until task is done
        while not done.is_set():
            delay(0.1)

        self._loop.close()
        self._thread.join()

        self.__init__(
            bot=self._bot,
            token=self._token
        )