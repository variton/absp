"""edatalake module."""

from enum import Enum


class EDataLake(Enum):
    """Enum to specify the type of database."""

    S3 = 0
    """S3 refers to aws S3."""
    GCS = 1
    """GCS refers to google cloud storage."""
    ADLS = 2
    """ADLS refers to azure data lake storage."""
    HDFS = 3
    """HDFS refers to hadoop cluster."""
