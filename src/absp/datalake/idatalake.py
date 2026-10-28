"""idatalake module."""

from absp.fmk.istorage import IStorage
from absp.datalake.datalakempr import DATALAKEMPR


class IDataLake(IStorage):
    def __init__(self, _mapper: dict = DATALAKEMPR):
        super().__init__(_mapper)
