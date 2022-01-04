# libodb

A client library for accessing the OpenDiscordBots API

## Example Usage

```py
from asyncio import run

from libodb import APIClient
from pydantic import BaseModel


class GuildConfig(BaseModel):
    test: str


async def main():
    c = APIClient("api_key")

    await c.kv_set("abc", "123")
    print(await c.kv_get("abc"))

    await c.set_guild_config(1234, "example", GuildConfig(test="test"))
    print(await c.get_guild_config(1234, "example", GuildConfig))

    await c.close()

run(main())
```
