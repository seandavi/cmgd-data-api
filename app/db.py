import clickhouse_connect
from .config import settings


async def get_clickhouse_client():
    client = await clickhouse_connect.create_async_client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DB,
    )
    return client
