"""edb module."""

from enum import Enum

class EDb(Enum):
    """Enum to specify the type of database."""

    MGDB = 0
    """MONGO(Multi Model) refers to mongodb."""
    PGRES = 1
    """PGRES refers to postgresql."""
    SQLE = 2
    """SQLE refers to sqlite."""
