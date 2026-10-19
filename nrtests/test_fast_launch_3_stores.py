
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
    
    stores = await asyncio.gather(iabsp.get("mongo",'http://localhost:2456', 'neo'),
                                  iabsp.get("redis","localhost",6379),
                                  iabsp.get("s3","x-bucket"))
    
    try:
        results = await asyncio.gather(*(store.connect() for store in stores))

        end = time.perf_counter()
        print(f"Execution time: {end - start:.6f} seconds")

        for result in results:
            assert result
    finally:
        await asyncio.gather(*(store.close() for store in stores))

