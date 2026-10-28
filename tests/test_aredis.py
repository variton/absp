import asyncio
import pytest
import pytest_asyncio
import json

from absp.iabsp import IAbsp

XUSERJSON = {
    "name": "neo",
    "password": "x245dev",
    "email": "neo@spectrum.io",
    "location": "Berlin",
}
XDATA = {"user:neo": json.dumps(XUSERJSON)}


@pytest.fixture
def iabsp():
    return IAbsp()


@pytest_asyncio.fixture
async def r_connection(iabsp):
    """Create a redis instance."""
    aredis = await iabsp.get("redis", "localhost", 6379)
    client = await aredis.connect()
    return aredis, client


@pytest.mark.asyncio
async def test_iabsp_get_redis_not_connected(r_connection):
    aredis, connection = r_connection
    try:
        is_connected = await connection.ping()
    except:
        is_connected = False
        assert is_connected == False
    await aredis.close()


@pytest.mark.asyncio
async def test_iabsp_redis_insert(r_connection):
    aredis, _ = r_connection
    await aredis.insert(**XDATA)
    await aredis.close()


# @pytest_asyncio.fixture(name="_redisawhe")
# @pytest.mark.asyncio
# async def redisawhe_fixture(_context):
#     """Create a RedisAwhe instance."""
#     # Create a RedisAwhe instance
#     l_redisawhe = await _context.get(EAwhe.REDIS)
#     # Setup: If testing database is not empty, flush it
#     if await l_redisawhe.count() > 0:
#         await l_redisawhe.client_.flushdb()
#     return l_redisawhe
