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
    async def __ainit__(self,_url:str="", _inm_name: str=""):
        print("") 
        if _url != "" :
            print(_url)
        if _inm_name != "":
            print(_inm_name)

    async def connect(self) -> bool:
        """
        Connect the client object to REDIS.

        Returns
        -------
            Indicate if the connection to REDIS was made.
        """
        print("connecting ot mongodb")
        return True
