
import asyncio
import pytest

from absp.inmemory.iinmemory import IInMemory 
from absp.inmemory.einmemory import EInMemory

@pytest.fixture
def iinmemory():
    return IInMemory()

@pytest.mark.asyncio
async def test_iinmemory_get(iinmemory):
    aredis_mock = await iinmemory.get(EInMemory.RMOCK)
    res = await aredis_mock.connect()
    assert res
    await aredis_mock.close()
