"""iabsp module."""

# PMPR={"inmemory":,
#       "db":,
#       "datalake":}

class IAbsp:
    """Interface to create & use absp store packages.

    Attribute
    ---------
    mapper_: dict
        The mapper of the package interface

    Methods
    -------
    __init__(_mapper)
        Set the init state of object with a mapper

    get(_earc,*args)
        create the needed warehouse asynchronously.
    """

    def __init__(self, _mapper=PMPR):
        """Initialiaze the object state with a mapper.

        Parameters
        ----------
        _mapper:
            The mapper of the package interface
        """
        self.mapper_ = _mapper

    async def get(self, _interface : str, *args) -> object:
        """Instance the warehouse asynchronously.

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
