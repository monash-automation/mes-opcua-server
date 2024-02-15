import asyncio

import flatdict
import redis
from opcuax import OpcuaModel, OpcuaServer
from redis.asyncio import Redis

from .models import Printer
from .settings import EnvSettings


async def run_server():
    settings = EnvSettings()
    redis_dsn = settings.opcua_server_redis_url

    redis_client: Redis = redis.asyncio.Redis(
        host=redis_dsn.host, port=redis_dsn.port, db=int(redis_dsn.path[1:])
    )

    server = OpcuaServer.from_settings(settings)

    async with server:
        printer1 = await server.create("Printer1", Printer())
        printer2 = await server.create("Printer2", Printer())
        printer3 = await server.create("Printer3", Printer())

        async def cache(key: str, model: OpcuaModel) -> None:
            while True:
                await server.refresh(model)
                data = flatdict.FlatDict(model.model_dump(), delimiter=".")
                data = {k: str(v) for k, v in data.items()}
                await redis_client.hset(key, mapping=data)
                await asyncio.sleep(1)

        _ = [
            asyncio.create_task(cache(key, model))
            for key, model in [
                ("Printer1", printer1),
                "Printer2",
                printer2,
                "Printer3",
                printer3,
            ]
        ]

        await server.loop()


def main():
    asyncio.run(run_server())
