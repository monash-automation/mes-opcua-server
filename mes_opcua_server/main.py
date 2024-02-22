import asyncio

import flatdict
import redis
from opcuax import OpcuaModel, OpcuaServer
from redis.asyncio import Redis

from .models import Printer, RobotArm
from .settings import EnvSettings


async def create_printers(server: OpcuaServer, n: int) -> dict[str, OpcuaModel]:
    def name(i: int) -> str:
        return f"Printer{i}"

    return {name(i): await server.create(name(i), Printer()) for i in range(n)}


async def create_robot_arms(server: OpcuaServer, n: int) -> dict[str, OpcuaModel]:
    def name(i: int) -> str:
        return f"Arm{i}"

    return {name(i): await server.create(name(i), RobotArm()) for i in range(1, n + 1)}


async def run_server() -> None:
    settings = EnvSettings()
    redis_dsn = settings.opcua_server_redis_url

    redis_client: Redis = redis.asyncio.Redis(
        host=redis_dsn.host, port=redis_dsn.port, db=int(redis_dsn.path[1:])
    )

    server = OpcuaServer.from_settings(settings)

    async with server:
        # Printer 0-7 for production, Printer 8-9 for testing
        printers = await create_printers(server, 10)
        arms = await create_robot_arms(server, 4)

        models = printers | arms

        async def cache(key: str, model: OpcuaModel) -> None:
            while True:
                await server.refresh(model)
                data = flatdict.FlatDict(model.model_dump(), delimiter=".")
                data = {k: str(v) for k, v in data.items()}
                await redis_client.hset(key, mapping=data)
                await asyncio.sleep(1)

        _ = {
            name: asyncio.create_task(cache(name, model))
            for name, model in models.items()
        }

        await server.loop()


def main() -> None:
    asyncio.run(run_server())
