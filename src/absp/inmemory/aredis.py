"""aredis module."""

from typing import Any

import redis.asyncio as redis
from async_class import AsyncObject


class ARedis(AsyncObject):
    """
    A class to give access to Redis in-memory storage.

    Attributes
    ----------
    client_ : aioredis.Redis
        The aioredis client object.

    Methods
    -------
    __ainit__(*args)
        Initialize the RedisAwhe class asynchronously.

    connect() -> bool
        Not implemented. Connection is established in __ainit__.

    insert(**kwargs) -> None
        Insert data into the Redis storage.

    find(_key: Any) -> bool
        Find data for a given key in Redis.

    get(_key: Any) -> Any
        Get data for a given key from Redis.

    update(**kwargs) -> None
        Update the value of data for a given key in Redis.

    delete(_key: Any) -> None
        Delete data for a given key from Redis.

    count() -> int
        Count the number of elements in the Redis storage.

    flush() -> bool
        Flush all the data stored in redis.

    search(_pattern:str) -> Any
        Search for all exists keys for a define pattern.

    """

    async def __ainit__(self,host:str,port:int,decode:bool=True) -> None:
        self.host_ = host
        self.port_ = port
        self.decode_ = decode
        self.client_ = None

    async def connect(self) -> None:  # pragma: no cover
        pass

    async def insert(self, **kwargs: Any) -> None:
        """
        Set data into the Redis storage.

        Parameters
        ----------
        **kwargs : dict
            Key : str
                The key for the data to be set.
            Value : Any
                The value for the data to be set.
        """
        await self.client_.set(kwargs["Key"], kwargs["Value"])

    async def find(self, _key: str) -> bool:
        """
        Find a given key in Redis.

        Parameters
        ----------
        _key : str
            The key to be found.

        Returns
        -------
        bool
            True if the key is found, False otherwise.
        """
        l_num = await self.client_.exists(_key)
        return l_num != 0

    async def get(self, _key: str) -> Any:
        """
        Get data for a given key from Redis.

        Parameters
        ----------
        _key : str
            The key for the data to be retrieved.
        """
        return await self.client_.get(_key)

    async def update(self, **kwargs: Any) -> None:
        """Not implemented for this class."""
        pass

    async def replace(self, _key: str, _value: Any) -> None:
        """
        Replace the value of data for a given key in Redis.

        Parameters
        ----------
        _key : str
            The key for the data to be updated.
        _value : Any
            The value for the new data to set.
        """
        await self.client_.set(_key, _value)

    async def delete(self, *_keys: str) -> None:
        """
        Delete data for one key or multiple keys from Redis.

        Parameters
        ----------
        *_keys : str
            The key(s) for the data to be deleted.
        """
        await self.client_.delete(*_keys)

    async def count(self) -> int:
        """
        Count the number of elements in the Redis storage.

        Returns
        -------
        int
            The number of elements in the Redis storage.
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
        l_number_of_objs = await self.count()
        if l_number_of_objs > 0:
            await self.client_.flushall()
            return True
        return False

    # todo write unit tests
    async def search(self, _pattern: str) -> Any:
        """
        Search for all exists keys for a define pattern.

        Returns
        -------
        Any
            Return a value or list of values.
        """
        return await self.client_.keys(_pattern)
