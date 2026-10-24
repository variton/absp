# Asynchronous Backend Store Package (ABSP)

ABSP is a Python package under development for creating asynchronous database,
in-memory, and data lake stores through a common factory.

## Available Backends

| Store key | Backend factory | Backend enum | Implementation |
| --- | --- | --- | --- |
| `"mongo"` | `IDb` | `EDb.MGDB` | `AMongoDbMock` |
| `"redis"` | `IInMemory` | `EInMemory.REDIS` | `ARedis` |
| `"rmock"` | `IInMemory` | `EInMemory.RMOCK` | `ARedisMock` |
| `"s3"` | `IDataLake` | `EDataLake.S3` | `AS3Mock` |

The MongoDB, Redis mock, and S3 implementations print connection information
and return `True` from `connect()`. They do not connect to servers or persist
data. The `"redis"` backend uses `redis.asyncio` to access a real Redis server.

PostgreSQL, SQLite, Dragonfly, Aerospike, Google Cloud Storage, Azure Data Lake
Storage, and HDFS have enum values but no mapped implementations. Unsupported
store keys or unmapped backend enum values raise `KeyError`.

## Getting Started

Python **3.14 or newer** and [uv](https://docs.astral.sh/uv/) are required for
the setup below. From the repository root:

```bash
uv sync
uv run python -c "import absp; print(absp.__file__)"
```

`uv sync` installs the package, runtime dependencies (`async-class`, `redis`,
and `xphide`), and the default development dependency group. The `xphide`
dependency is sourced from its Git repository at tag `v0.1.0`, as configured in
`pyproject.toml`.

## Usage

### Mock stores

This example requires no external services:

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("mongo", "mongodb://localhost:27017", "example")
    try:
        connected = await store.connect()
        print(connected)  # True: this is a mock connection.
    finally:
        await store.close()


asyncio.run(main())
```

Use either of these factory calls inside an async function for the other mocks:

```python
redis_mock = await IAbsp().get("rmock")  # Defaults to localhost:6379.
s3_mock = await IAbsp().get("s3", "example-bucket")
```

Each mock supports the same `connect()` and `close()` lifecycle. The MongoDB
mock also accepts an optional third argument for models; the S3 mock accepts
an optional client argument after the bucket name.

### Redis

The real Redis backend requires a host and port. `connect()` returns an
asynchronous Redis client; use `ping()` to verify that the server is reachable.

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("redis", "localhost", 6379)
    client = await store.connect()
    try:
        await client.ping()
        await store.insert(**{"example:message": "hello"})
        print(await client.get("example:message"))
        await store.delete("example:message")
    finally:
        await client.aclose()
        await store.close()


asyncio.run(main())
```

The Redis wrapper provides `insert`, `find`, `replace`, `delete`, `count`,
`flush`, and `search`. It is still incomplete: `update()` is a no-op and
`get()` currently references an undefined variable. Use the returned client's
`get()` method, as above. `insert()` writes only the first keyword argument;
`flush()` calls Redis `FLUSHALL`, clearing all databases on the server.

### Backend-specific factories

You can also create stores directly through the corresponding factory:

```python
from absp.db.edb import EDb
from absp.db.idb import IDb
from absp.inmemory.einmemory import EInMemory
from absp.inmemory.iinmemory import IInMemory
from absp.datalake.edatalake import EDataLake
from absp.datalake.idatalake import IDataLake

# Inside an async function:
mongo = await IDb().get(EDb.MGDB, "mongodb://localhost:27017", "example")
redis_mock = await IInMemory().get(EInMemory.RMOCK)
s3 = await IDataLake().get(EDataLake.S3, "example-bucket")
```

Close each store after use with `await store.close()`.

## Development

Run the tests and generate a self-contained HTML report:

```bash
uv run bash local-ci.sh
```

The script creates `reports/` if needed and writes `reports/report.html`.
To run tests without generating a report:

```bash
uv run pytest
```

The full suite includes a Redis insertion test that requires a running Redis
server at `localhost:6379`. To run only tests using mock backends:

```bash
uv run pytest tests/test_idb.py tests/test_inmemory.py tests/test_idatalake.py tests/test_iabsp.py -k 'not redis'
```

Additional sequential and concurrent store-launch tests are in `nrtests/`:

```bash
uv run pytest nrtests
```

These construct a real Redis client, but do not verify server connectivity
with a Redis command.

## Repository Layout

```text
pyproject.toml       Package metadata, dependency groups, and build configuration
uv.lock              Locked dependencies
local-ci.sh          Pytest execution and HTML report generation
src/absp/
    iabsp.py         Store factory (mongo, redis, rmock, and s3)
    fmk/             Shared storage factory base class
    db/              Database factory, backend enum, mapper, and MongoDB mock
    inmemory/        In-memory factory, Redis client, and Redis mock
    datalake/        Data lake factory, backend enum, mapper, and S3 mock
tests/               Factory, mock, and Redis tests
nrtests/             Sequential and concurrent store-launch tests
reports/             Generated test reports (report.html is ignored by Git)
```
