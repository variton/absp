
import asyncio
import pytest

from absp.iabsp import IAbsp  

@pytest.fixture
def iabsp():
    return IAbsp()

@pytest.mark.asyncio
async def test_iabsp_get_mongo(iabsp):
    amongodb_mock = await iabsp.get("mongo",'http://localhost:2456', 'neo')
    res = await amongodb_mock.connect()
    assert res
    await amongodb_mock.close()

@pytest.mark.asyncio
async def test_iabsp_get_redis(iabsp):
    aredis_mock = await iabsp.get("redis")
    res = await aredis_mock.connect()
    assert res
    await aredis_mock.close()

@pytest.mark.asyncio
async def test_iabsp_get_s3(iabsp):
    as3_mock = await iabsp.get("s3","x-bucket")
    res = await as3_mock.connect()
    assert res
    await as3_mock.close()
