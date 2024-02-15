from opcuax.settings import EnvOpcuaServerSettings
from pydantic import RedisDsn


class EnvSettings(EnvOpcuaServerSettings):
    opcua_server_redis_url: RedisDsn = "redis://localhost:6379/0"
