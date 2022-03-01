from asyncio import Task, create_task, sleep
from os import getenv

from aiohttp import ClientSession
from loguru import logger


class StatusHeartbeater:
    def __init__(self) -> None:
        self._call_uri: str | None = getenv("STATUS_CALL_URI")
        self._task: Task | None = None
        self._session: ClientSession | None = None

    async def _heartbeat(self) -> None:
        if not self._call_uri:
            return

        while True:
            try:
                if not self._session:
                    self._session = ClientSession()

                await self._session.get(self._call_uri)
                logger.info(f"Sent status heartbeat.")

                await sleep(45)
            except Exception as e:
                logger.error(e)

    def run(self) -> None:
        if self._call_uri:
            self._task = create_task(self._heartbeat())

    def stop(self) -> None:
        if self._task:
            self._task.cancel()
