"""amongodb_mock module."""
# multiple model mongo-db asynchronous store

import os
import asyncio
from typing import Any, List

from async_class import AsyncObject

class AMongoDbMock(AsyncObject):
    """
    A class that implements the interfaces exposed by the async mongo driver.
    """
    async def __ainit__(self,_url:str="", _db_name: str="", _models=None):
        print("") 
        if _url != "" :
            print(_url)
        if _db_name != "":
            print(_db_name)

    async def connect(self) -> bool:
        """
        Connect the client object to MONGODB.

        Returns
        -------
            Indicate if the connection to MONGODB was made.
        """
        print("connecting ot mongodb")
        return True
