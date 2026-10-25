# Asynchronous Backend Store Package (ABSP)

ABSP is a Python package under development for creating asynchronous storage
adapters through a common factory. It currently includes a Redis adapter and
connection mocks for MongoDB, Redis, and Amazon S3.

## Available backends

Use `await IAbsp().get(key, *args)` to create an adapter:

| Store key | Implementation | Constructor arguments | External service |
| --- | --- | --- | --- |
| `"mongo"` | `AMongoDbMock` | URL, database name, optional models | None (mock) |
| `"rmock"` | `ARedisMock` | Host (default `"localhost"`), port (default `6379`) | None (mock) |
| `"redis"` | `ARedis` | Host, port, optional decode flag (default `True`) | Redis |
| `"s3"` | `AS3Mock` | Bucket name, optional client | None (mock) |

The mocks print connection information and return `True` from `connect()`;
they do not persist data. The Redis adapter uses `redis.asyncio` and exposes
operations including `insert`, `find`, `replace`, `delete`, `count`, and `search`.

PostgreSQL, SQLite, Dragonfly, Aerospike, GCS, ADLS, and HDFS have enum values
but no mapped implementations. Unsupported store keys and unmapped enum values
raise `KeyError`. The backend-specific factory and enum pairs are `IDb` /
`EDb.MGDB` for MongoDB, `IInMemory` / `EInMemory.REDIS` or
`EInMemory.RMOCK` for Redis, and `IDataLake` / `EDataLake.S3` for S3.

## Setup

Requirements: **Python 3.14 or newer**, Git (for the `xphide` dependency), and
`uv`. Run these commands from the repository root:

```bash
uv sync --locked
uv run python -c "import absp; print(absp.__file__)"
```

`uv sync` creates a project virtual environment and installs the package and
the default `dev` dependency group using `uv.lock`. Runtime dependencies are
`async-class`, `redis`, and `xphide`. The `xphide` source is configured in
`pyproject.toml` as a Git dependency pinned to tag `v0.1.0`.

To install without development tools:

```bash
uv sync --locked --no-dev
```

## Quick start: no server required

Save this example as `example.py` and run it with `uv run python example.py`:

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("rmock")
    try:
        connected = await store.connect()
        print(connected)  # True: this is a mock connection.
    finally:
        await store.close()


asyncio.run(main())
```

To try another mock, replace the store creation line with either:

```python
store = await IAbsp().get("mongo", "mongodb://localhost:27017", "example")
store = await IAbsp().get("s3", "example-bucket")
```

The mock arguments are only used for printed connection information. No MongoDB
server, AWS credentials, or S3 bucket is required.

## Using Redis

Start a Redis server reachable at `localhost:6379`, then run this example:

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("redis", "localhost", 6379)
    client = await store.connect()
    try:
        await client.ping()
        await store.insert(**{"absp:example": "hello"})
        print(await store.find("absp:example"))  # True
        print(await client.get("absp:example"))  # hello
        await store.delete("absp:example")
    finally:
        await client.aclose()
        await store.close()


asyncio.run(main())
```

`connect()` returns a Redis client; it does not verify connectivity. The first
command, such as `ping()`, contacts the server. Pass `False` as the third factory
argument to receive bytes instead of decoded strings.

The Redis adapter is incomplete: `get(key)` currently references an undefined
variable, and `update()` is a no-op. Use the returned client's `get(key)` to read
values, as above. `insert()` writes only the first keyword argument.
`flush()` calls Redis `FLUSHALL` when the selected database is
nonempty, so it can remove data across all databases on the server.

## Backend-specific factories

The top-level factory delegates to factories that can also be used directly.
Inside an async function:

```python
from absp.datalake.edatalake import EDataLake
from absp.datalake.idatalake import IDataLake
from absp.db.edb import EDb
from absp.db.idb import IDb
from absp.inmemory.einmemory import EInMemory
from absp.inmemory.iinmemory import IInMemory

mongo = await IDb().get(EDb.MGDB, "mongodb://localhost:27017", "example")
redis_mock = await IInMemory().get(EInMemory.RMOCK)
s3 = await IDataLake().get(EDataLake.S3, "example-bucket")
```

Close each adapter with `await adapter.close()` after use. For a real Redis
connection, also close the returned client with `await client.aclose()`.

## Development and tests

Install development dependencies with `uv sync --locked`. To run only the mock
tests, without any external services:

```bash
uv run pytest tests/test_idb.py tests/test_idatalake.py tests/test_inmemory.py tests/test_iabsp.py::test_iabsp_get_mongo tests/test_iabsp.py::test_iabsp_get_s3
```

The full suite includes Redis tests that connect to `localhost:6379` and write
data. Use a disposable Redis instance:

```bash
uv run pytest
```

Generate a self-contained HTML report at `reports/report.html`:

```bash
uv run bash local-ci.sh
```

The script creates `reports/` if needed. The generated report is ignored by Git.
The `nrtests/` directory contains additional sequential and concurrent store
creation tests; pytest's default discovery includes these tests as well.
To run them separately:

```bash
uv run pytest nrtests
```

These tests construct a real Redis client but do not verify server connectivity
with a Redis command.

## Repository layout

```text
pyproject.toml       Package metadata, dependencies, and build configuration
uv.lock              Locked dependency versions
local-ci.sh          Pytest runner with HTML report generation
src/absp/
    iabsp.py         Top-level store factory
    fmk/             Shared storage factory base class
    datalake/        Data lake factory, backend enum, and S3 mock
    db/              Database factory, backend enum, and MongoDB mock
    inmemory/        In-memory factory, backend enum, Redis adapter and mock
tests/               Factory, mock, and Redis tests
nrtests/             Sequential and concurrent store creation tests
reports/             Generated test reports
```
