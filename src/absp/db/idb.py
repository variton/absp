"""idb module."""

from absp.fmk.istorage import IStorage
from absp.db.dbmpr import DBMPR

class IDb(IStorage):
    def __init__(self, _mapper:dict=DBMPR):
        super().__init__(_mapper)
