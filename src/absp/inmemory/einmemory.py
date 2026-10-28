"""einmemory module."""

from enum import Enum


class EInMemory(Enum):
    """Enum to specify the type of in memory store."""

    REDIS = 0
    """REDIS refers to redis in memory cache."""
    DRFLY = 1
    """DRFLY refers to dragonfly."""
    AEROS = 2
    """AEROS refers to aerospike."""
    RMOCK = 3
    """RMOCK refers to aredis_mock."""
