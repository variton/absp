
import asyncio
import pytest

from absp.iabsp import IAbsp  

@pytest.fixture
def iabsp():
    return IAbsp()

@pytest.mark.asyncio
async def test_iabsp_get(iabsp):
    amongodb_mock = await iabsp.get("mongo",'http://localhost:2456', 'neo')
    res = await amongodb_mock.connect()
    assert res
    await amongodb_mock.close()
