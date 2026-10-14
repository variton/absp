"""iinmemory module."""

from absp.fmk.istorage import IStorage
from absp.inmemory.inmemorympr import INMEMORYMPR

class IInMemory(IStorage):
    def __init__(self, _mapper:dict=INMEMORYMPR):
        super().__init__(_mapper)
