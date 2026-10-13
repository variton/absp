"""iinmemory module."""

from absp.inmemory.einmemory import EInMemory
from absp.inmemory.inmemorympr import INMEMORYMPR

class IInMemory:
    """Interface to create & use inmemory objects.

    Attribute
    ---------
    mapper_: dict
        The mapper of the package interface

    Methods
    -------
    __init__(_mapper)
        Set the init state of object with a mapper

    get(_einmemory,*args)
        create the needed in memory store asynchronously.
    """

    def __init__(self, _mapper=INMEMORYMPR):
        """Initialiaze the object state with a mapper.

        Parameters
        ----------
        _mapper:
            The mapper of the package interface
        """
        self.mapper_ = _mapper

    async def get(self, _einmemory: EInMemory, *args) -> object:
        """Instance the in memory object  asynchronously.

        Parameter
        ---------
        _einmemory: EInMemory 
            type of in memory store 

        *args:
            arguments needed to create the inmemory store 

        Raises
        -------
        KeyError
            if the key doesn't exist
        """
        return await self.mapper_[_einmemory](*args)
