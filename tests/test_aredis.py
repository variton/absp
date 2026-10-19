
import asyncio
import pytest

from absp.iabsp import IAbsp  

@pytest.fixture
def iabsp():
    return IAbsp()

@pytest.mark.asyncio
async def test_iabsp_get_redis(iabsp):
    aredis = await iabsp.get("redis","localhost", 6379)
    res = await aredis.connect()
    assert res
    await aredis.close()
