"""dbmpr module."""

from absp.db.edb import EDb

# from absp.db.amongodb import AMongoDb
from absp.db.amongodb_mock import AMongoDbMock

"""MAPPER for DBMPR interface."""
DBMPR = {
    EDb.MGDB: AMongoDbMock,
}

#   EDb.MGDB: AMongoDb,
#   EDb.PGRES: APostGreSql,
#   EDb.SQLE: ASqlite,
