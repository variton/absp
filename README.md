# Asynchronous Backend Store Package (ABSP)

ABSP is a Python package for creating asynchronous storage adapters through a
shared factory interface. It provides a Redis adapter and connection mocks for
MongoDB, Redis, and Amazon S3.

**Status:** Early development. Backend support and Redis operations are incomplete;
review the [current limitations](#current-limitations) before integrating ABSP.

## Backend support

Create an adapter with `await IAbsp().get(key, *args)`.

| Key | Adapter | Factory arguments | Service required |
| --- | --- | --- | --- |
| `"redis"` | `ARedis` | Host, port, optional decode flag (`True` by default) | Redis |
| `"rmock"` | `ARedisMock` | Optional host (`"localhost"`) and port (`6379`) | None |
| `"mongo"` | `AMongoDbMock` | Optional URL, database name, and models | None |
| `"s3"` | `AS3Mock` | Optional bucket name and client | None |

The mocks print connection information and return `True` from `connect()`. They
do not connect to external services or persist data.

## Installation

Requirements:

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- Git, for the `xphide` dependency

From the repository root, install the package and development dependencies:

```bash
uv sync --locked
```

For a runtime-only environment:

```bash
uv sync --locked --no-dev
```

Runtime dependencies are `async-class`, `redis`, and `xphide`. The `xphide`
dependency is sourced from Git and pinned to tag `v0.1.1` in `pyproject.toml`.

## Quick start

This example uses the Redis mock and requires no external service. Save it as
`example.py`:

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("rmock")
    try:
        connected = await store.connect()
        print(connected)  # True
    finally:
        await store.close()


asyncio.run(main())
```

Run the example:

```bash
uv run python example.py
```

To use a different mock, replace the adapter creation line with one of these:

```python
store = await IAbsp().get("mongo", "mongodb://localhost:27017", "example")
store = await IAbsp().get("s3", "example-bucket")
```

These examples require neither a MongoDB server nor AWS credentials.

## Redis usage

With a Redis server available at `localhost:6379`:

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

`connect()` returns a `redis.asyncio` client. Connectivity is checked when a
command such as `ping()` runs. Pass `False` after the host and port to receive
bytes instead of decoded strings:

```python
store = await IAbsp().get("redis", "localhost", 6379, False)
```

The adapter exposes `insert`, `find`, `replace`, `delete`, `count`, and `search`.
Use the returned client's `get()` to read values while the adapter's `get()`
remains incomplete.

## Backend-specific factories

Use a backend-specific factory when working directly with its enum. The following
calls belong inside an async function:

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

Call `await adapter.close()` after use. For the real Redis adapter, also close
the returned client with `await client.aclose()`.

## Current limitations

- MongoDB and S3 support consists of connection mocks only.
- PostgreSQL, SQLite, Dragonfly, Aerospike, GCS, ADLS, and HDFS have enum entries
  but no mapped implementations. Unsupported keys and unmapped enum values raise
  `KeyError`.
- Redis `get()` references an undefined variable; use `client.get(key)` instead.
- Redis `assign()` and `update()` are not implemented.
- Redis `insert()` writes only the first keyword argument.
- Redis `flush()` issues `FLUSHALL` when the selected database is nonempty. This
  can delete data across all databases on the server.

## Development

Install development dependencies with `uv sync --locked`.

### Tests

Run the mock tests without external services:

```bash
uv run pytest tests/test_idb.py tests/test_idatalake.py tests/test_inmemory.py tests/test_iabsp.py::test_iabsp_get_mongo tests/test_iabsp.py::test_iabsp_get_s3
```

The full suite includes tests that write to Redis at `localhost:6379`. Use a
disposable Redis instance:

```bash
uv run pytest
```

Additional sequential and concurrent adapter creation tests live in `nrtests/`.
Pytest includes them in default discovery; they can also be run separately:

```bash
uv run pytest nrtests
```

These additional tests construct a Redis client without issuing commands to
verify server connectivity.

### Local CI

Run the formatting check, test suites, and coverage report:

```bash
uv run bash local-ci.sh
```

The script installs dependencies with `uv sync`, checks formatting with Black,
runs `tests/` and `nrtests/` separately, and generates these reports:

| Report | Path |
| --- | --- |
| Unit tests | `reports/unit-tests.html` |
| Integration tests | `reports/integration-tests.html` |
| Coverage | `reports/coverage/index.html` |

Each run replaces the existing `reports/` directory.

## Repository structure

```text
src/absp/
    iabsp.py         Top-level adapter factory
    fmk/             Shared storage factory base class
    datalake/        Data lake factory, backend enum, and S3 mock
    db/              Database factory, backend enum, and MongoDB mock
    inmemory/        In-memory factory, backend enum, Redis adapter and mock
tests/               Factory, mock, and Redis tests
nrtests/             Sequential and concurrent adapter creation tests
local-ci.sh          Formatting, tests, and coverage workflow
pyproject.toml       Package metadata, dependencies, and build configuration
uv.lock              Locked dependency versions
```
