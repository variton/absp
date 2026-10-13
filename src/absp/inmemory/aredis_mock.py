"""aredis_mock module."""
# multiple model mongo-db asynchronous store

import os
import asyncio
from typing import Any, List

from async_class import AsyncObject

class ARedisMock(AsyncObject):
    """
    A class that implements the interfaces exposed by the async redis driver.
    """
    async def __ainit__(self,_host:str="localhost", _port:int=6379):
        print("") 
        if _host:
            print(_host)
        if _port:
            print(_port)

    async def connect(self) -> bool:
        """
        Connect the client object to REDIS.

        Returns
        -------
            Indicate if the connection to REDIS was made.
        """
        print("connecting to redis")
        return True
