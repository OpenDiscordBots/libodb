from json import dumps
from typing import Any, Optional, Type, TypeVar, Union

from aiohttp import ClientSession
from pydantic import BaseModel

URL = "https://api.opendiscordbots.com"
T = TypeVar("T")


class APIClient:
    def __init__(self, key: str, *, kv_ns: str = "", url: str = URL) -> None:
        self._key = key

        self._kv_ns = kv_ns
        self._url = url

        self.__session: Optional[ClientSession] = None

    @property
    def _session(self) -> ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = ClientSession(headers={
                "Authorization": self._key
            })

        return self.__session

    def kv_key(self, key: str) -> str:
        if not self._kv_ns:
            return key

        return f"{self._kv_ns}.{key}"

    async def close(self) -> None:
        if self.__session is not None:
            await self.__session.close()

    async def kv_set(self, key: str, value: str) -> None:
        await self._session.post(f"{self._url}/kv/{self.kv_key(key)}", data=dumps(value))

    async def kv_get(self, key: str) -> Any:
        resp = await self._session.get(f"{self._url}/kv/{self.kv_key(key)}")

        if resp.status == 404:
            return None

        resp.raise_for_status()

        return await resp.json()

    async def get_guild_config(self, guild: int, module: str, model: Type[T]) -> Union[T, None]:
        if not issubclass(model, BaseModel):
            raise TypeError("Model must be a subclass of pydantic.BaseModel")

        resp = await self._session.get(f"{self._url}/guilds/{guild}/config/{module}")

        if resp.status == 404:
            return None

        resp.raise_for_status()

        return model(**(await resp.json()))

    async def set_guild_config(self, guild: int, module: str, value: Any) -> None:
        if isinstance(value, BaseModel):
            value = value.dict()
        await self._session.post(f"{self._url}/guilds/{guild}/config/{module}", data=dumps(value))
