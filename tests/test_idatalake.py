
import asyncio
import pytest

from absp.datalake.idatalake import IDataLake
from absp.datalake.edatalake import EDataLake

@pytest.fixture
def idatalake():
    return IDataLake()

@pytest.mark.asyncio
async def test_iinmemory_get(idatalake):
    as3_mock = await idatalake.get(EDataLake.S3,"x-bucket")
    res = await as3_mock.connect()
    assert res
    await as3_mock.close()
