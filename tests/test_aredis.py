
import asyncio
import pytest

from absp.iabsp import IAbsp  

@pytest.fixture
def iabsp():
    return IAbsp()

@pytest.mark.asyncio
async def test_iabsp_get_redis_not_connected(iabsp):
    aredis = await iabsp.get("redis","localhost", 6379)
    client = await aredis.connect()
    
    try:
        is_connected = await client.ping()
    except:
        is_connected = False 
    assert is_connected == False
    await aredis.close()
