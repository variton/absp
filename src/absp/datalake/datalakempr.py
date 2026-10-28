"""datalakempr module."""

from absp.datalake.edatalake import EDataLake
from absp.datalake.as3_mock import AS3Mock

"""MAPPER for DBMPR interface."""
DATALAKEMPR = {
    EDataLake.S3: AS3Mock,
}
