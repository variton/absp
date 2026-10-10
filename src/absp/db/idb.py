"""idb module."""

from absp.db.edb import EDb
from absp.db.dbmpr import DBMPR
from absp.db.amongodb_mock import AMongoDbMock

class IDb:
    """Interface to create & use awhe objects.

    Attribute
    ---------
    mapper_: dict
        The mapper of the package interface

    Methods
    -------
    __init__(_mapper)
        Set the init state of object with a mapper

    get(_edb,*args)
        create the needed warehouse asynchronously.
    """

    def __init__(self, _mapper=DBMPR):
        """Initialiaze the object state with a mapper.

        Parameters
        ----------
        _mapper:
            The mapper of the package interface
        """
        self.mapper_ = _mapper

    async def get(self, _edb: EDb, *args) -> object:
        """Instance the db asynchronously.

        Parameter
        ---------
        _edb: EDb
            type of database

        *args:
            arguments needed to create the database

        Raises
        -------
        KeyError
            if the key doesn't exist
        """

        #__import__('pdb').set_trace()
        return await self.mapper_[_edb](*args)
