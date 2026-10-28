import asyncio
import pytest

from absp.db.idb import IDb
from absp.db.edb import EDb


@pytest.fixture
def idb():
    return IDb()


@pytest.mark.asyncio
async def test_idb_get(idb):
    amongodb_mock = await idb.get(EDb.MGDB, "http://localhost:2456", "neo")
    res = await amongodb_mock.connect()
    assert res
    await amongodb_mock.close()
