"""redis module."""

from typing import Any

import redis.asyncio as redis
from async_class import AsyncObject


class ARedis(AsyncObject):
    """
    A class to give access to Redis in-memory storage.

    """

    async def __ainit__(self,host:str,port:int,decode:bool=True) -> None:
        self.host_ = host
        self.port_ = port
        self.decode_ = decode
        self.client_ = None

    async def connect(self) -> object:
        self.client_ = redis.Redis(host=self.host_, 
                                   port=self.port_, 
                                   decode_responses=self.decode_)
        return self.client_ 

    async def insert(self, **kwargs: Any) -> None:
        """
        Set data into the Redis storage.

        Parameters
        ----------
        **kwargs : dict
        """
        key, value = next(iter(kwargs.items())) 
        await self.client_.set(key,value)

    async def find(self, key: str) -> bool:
        """
        Find a given key in Redis.

        """
        num = await self.client_.exists(key)
        return num != 0

    async def get(self, key: str) -> object:
        """
        Get data for a given key from Redis.

        """
        return await self.client_.get(_key)

    async def update(self, **kwargs: Any) -> None:
        """Not implemented for this class."""
        pass

    async def replace(self, key: str, value: object) -> None:
        """
        Replace the value of data for a given key in Redis.

        Parameters
        ----------
        _key : str
            The key for the data to be updated.
        _value : Any
            The value for the new data to set.
        """
        await self.client_.set(key,value)

    async def delete(self, *keys: str) -> None:
        """
        Delete data for one key or multiple keys from Redis.

        """
        await self.client_.delete(*keys)

    async def count(self) -> int:
        """
        Count the number of elements in the Redis storage.

        """
        return await self.client_.dbsize()

    async def flush(self) -> bool:
        """
        Flush all the objects contained the redis.

        Returns
        -------
        bool
            Return true if the operation succeded.

        """
        number_of_objs = await self.count()
        if number_of_objs > 0:
            await self.client_.flushall()
            return True
        return False

    # todo write unit tests
    async def search(self, pattern: str) -> Any:
        """
        Search for all exists keys for a define pattern.

            Return a value or list of values.
        """
        return await self.client_.keys(pattern)
