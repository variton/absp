"""as3_mock module."""

import os
import asyncio
from typing import Any, List

from async_class import AsyncObject

class AS3Mock(AsyncObject):
    """
    A class that implements the interfaces exposed by the async aws S3 driver.
    """
    async def __ainit__(self,_bucket:str="", _client: object=None):
        print("")
        if _bucket != "" :
            print(_bucket)

    async def connect(self) -> bool:
        """
        Connect the client object to S3.

        Returns
        -------
            Indicate if the connection to S3 was made.
        """
        print("connecting to S3")
        return True
