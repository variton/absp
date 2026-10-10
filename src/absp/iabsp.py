"""iabsp module."""

from functools import partial

class IAbsp:
    """Interface to create & use absp store packages.

    Methods
    -------
    __init__()
        Set the init state of object

    get(_earc,*args)
        create the needed store asynchronously.
    """

    def __init__(self):
        """Initialize the store mapper with database factory methods."""
        from absp.db.edb import EDb
        from absp.db.idb import IDb

        self.mapper_ = {"mongo": partial(IDb().get, EDb.MGDB)}

    async def get(self, _interface : str, *args) -> object:
        """Instance the store asynchronously.

        Parameter
        ---------
        _interface: a store interface 

        *args:
            arguments needed to create the store 

        Raises
        -------
        KeyError
            if the key doesn't exist
        """
        return await self.mapper_[_interface](*args)
