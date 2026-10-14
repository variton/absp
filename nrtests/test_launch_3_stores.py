
import asyncio
import pytest

from absp.iabsp import IAbsp  

import time

@pytest.fixture
def iabsp():
    return IAbsp()

@pytest.mark.asyncio
async def test_iabsp_get_stores(iabsp):

    start = time.perf_counter()

    amongodb_mock = await iabsp.get("mongo",'http://localhost:2456', 'neo')
    aredis_mock = await iabsp.get("redis")
    as3_mock = await iabsp.get("s3","x-bucket")
    
    res_mongo = await amongodb_mock.connect()
    res_redis = await aredis_mock.connect()
    res_s3 = await as3_mock.connect()

    end = time.perf_counter()
    print(f"Execution time: {end - start:.6f} seconds") 

    assert res_mongo
    assert res_redis
    assert res_s3

    await amongodb_mock.close()
    await aredis_mock.close()
    await as3_mock.close()
