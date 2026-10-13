"""inmemorympr module."""

from absp.inmemory.einmemory import EInMemory 
#from absp.inmemory.aredis import ARedis
from absp.inmemory.aredis_mock import ARedisMock

"""MAPPER for INMEMORYMPR interface."""
INMEMORYMPR = {
    EInMemory.REDIS: ARedisMock,
}
