from __future__ import annotations

from typing import Optional, Type, TypeVar

from aiohttp import ClientSession

from .models import Guild, JoinMessage, ServiceConfig, Todo
from .utils import model

T = TypeVar("T")


class ODBClient:
    def __init__(self, token: str, *, api_url: Optional[str] = None) -> None:
        self._token = token
        self._api_url = api_url or "https://canary.opendiscordbots.com/api"

        self.__session: Optional[ClientSession] = None

    @property
    def _session(self) -> ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = ClientSession()

        return self.__session

    async def __aenter__(self) -> ODBClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self.__session is not None and not self.__session.closed:
            await self.__session.close()

    async def _request(
        self, method: str, route: str, *, t: Type[T] = None, **kwargs
    ) -> T:
        async with self._session.request(
            method,
            self._api_url + route,
            headers={
                "Authorization": self._token,
            },
            **kwargs,
        ) as resp:
            resp.raise_for_status()

            data = await resp.json()

            if t is None:
                return data

            if not isinstance(data, t):
                raise TypeError(f"Expected {t}, got {type(data)}")

            return data

    @model(Guild)
    async def create_guild(self, guild_id: int) -> dict:
        return await self._request("POST", f"/guilds/", json={"id": guild_id}, t=dict)

    @model(Guild)
    async def get_guild(self, guild_id: int) -> dict:
        return await self._request("GET", f"/guilds/{guild_id}", t=dict)

    async def delete_guild(self, guild_id: int) -> None:
        await self._request("DELETE", f"/guilds/{guild_id}")

    @model(Guild)
    async def update_guild(self, guild_id: int, banned: bool) -> dict:
        data = {
            "banned": banned,
        }

        return await self._request("PATCH", f"/guilds/{guild_id}", json=data, t=dict)

    @model(ServiceConfig)
    async def create_service_config(
        self, guild_id: int, service: str, config: dict
    ) -> dict:
        return await self._request(
            "POST",
            f"/guilds/{guild_id}/config/{service}",
            json={
                "data": config,
            },
            t=dict,
        )

    @model(ServiceConfig)
    async def get_service_config(self, guild_id: int, service: str) -> dict:
        return await self._request(
            "GET", f"/guilds/{guild_id}/config/{service}", t=dict
        )

    async def delete_service_config(self, guild_id: int, service: str) -> None:
        await self._request("DELETE", f"/guilds/{guild_id}/config/{service}")

    @model(ServiceConfig)
    async def update_service_config(
        self, guild_id: int, service: str, config: dict
    ) -> dict:
        return await self._request(
            "PATCH",
            f"/guilds/{guild_id}/config/{service}",
            json={
                "data": config,
            },
            t=dict,
        )

    @model(JoinMessage)
    async def create_join_message(
        self, guild_id: int, member_id: int, channel_id: int, message_id: int
    ) -> dict:
        return await self._request(
            "POST",
            f"/services/cleanleave/guilds/{guild_id}/members/{member_id}",
            json={
                "channel_id": channel_id,
                "message_id": message_id,
            },
            t=dict,
        )

    @model(JoinMessage)
    async def get_join_message(self, guild_id: int, member_id: int) -> dict:
        return await self._request(
            "GET", f"/services/cleanleave/guilds/{guild_id}/members/{member_id}", t=dict
        )

    async def delete_join_message(self, guild_id: int, member_id: int) -> None:
        await self._request(
            "DELETE", f"/services/cleanleave/guilds/{guild_id}/members/{member_id}"
        )
