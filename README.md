# Asynchronous Backend Store Package (ABSP)

A Python package under development for asynchronous backend storage.

## Overview

ABSP aims to provide asynchronous backend storage functionality through the
`absp` Python package, with subpackages for data lakes, databases, and in-memory
storage.

## Project Status

The package currently provides asynchronous store factories (`IAbsp`, `IDb`,
and `IInMemory`) and mocks for MongoDB (`AMongoDbMock`) and Redis (`ARedisMock`).
Both mocks print connection information and return `True` from `connect()`;
they do not connect to a server or implement data persistence.

| Store key | Backend factory | Backend enum | Implementation |
| --- | --- | --- | --- |
| `"mongo"` | `IDb` | `EDb.MGDB` | `AMongoDbMock` |
| `"redis"` | `IInMemory` | `EInMemory.REDIS` | `ARedisMock` |

PostgreSQL, SQLite, Dragonfly, and Aerospike have enum values but no mapped
implementations. The `datalake` subpackage remains a skeleton. Four asynchronous
tests exercise both mocks through the store and backend-specific factories.

## Requirements

| Component | Version |
| --- | --- |
| Python | 3.14 or newer |

## Getting Started

From the repository root, create a virtual environment with Python 3.14 and
install the package in editable mode:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install async-class
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in
PowerShell instead.

The project currently declares development, testing, linting, security, and
documentation tools as package dependencies, so installation includes those
tools. The MongoDB mock also imports `AsyncObject` from `async_class`; its
`async-class` dependency is not yet declared in `pyproject.toml`, so install it
separately as shown above.

Verify that the package can be imported:

```bash
python -c "import absp; print(absp.__file__)"
```

## Usage

Create the MongoDB mock through the store factory:

```python
import asyncio

from absp.iabsp import IAbsp


async def main():
    store = await IAbsp().get("mongo", "http://localhost:2456", "neo")
    try:
        connected = await store.connect()
        print(connected)  # True: this is a mock connection.
    finally:
        await store.close()


asyncio.run(main())
```

The URL and database name are printed by the mock; no running MongoDB server is
required. The MongoDB mock accepts an optional third argument for models.

To use the Redis mock, replace the store creation line with:

```python
store = await IAbsp().get("redis", "localhost", 6379)
```

Redis defaults to host `"localhost"` and port `6379`, so
`await IAbsp().get("redis")` also works. Its host and port are printed by the
mock; no running Redis server is required. Use the same `connect()` and `close()`
lifecycle as in the MongoDB example.

You can also create either mock through its backend-specific factory:

```python
from absp.db.edb import EDb
from absp.db.idb import IDb
from absp.inmemory.einmemory import EInMemory
from absp.inmemory.iinmemory import IInMemory

# Inside an async function:
mongo = await IDb().get(EDb.MGDB, "http://localhost:2456", "neo")
redis = await IInMemory().get(EInMemory.REDIS, "localhost", 6379)
```

Close each mock with `await mock.close()` after use. Unsupported store names or
unmapped backend enum values raise `KeyError`.

## Repository Layout

```text
pyproject.toml       Package metadata, dependencies, and build configuration
local-ci.sh         Local test execution and HTML report generation
src/absp/           Main Python package
    iabsp.py        Asynchronous store factory ("mongo" and "redis")
    datalake/       Data lake package skeleton
    db/             Database factory, backend enum, mapper, and MongoDB mock
    inmemory/       In-memory factory, backend enum, mapper, and Redis mock
tests/              Four asynchronous factory and mock connection tests
reports/            Generated test reports (report.html is ignored by Git)
```

## Development

Before pushing a branch, activate the virtual environment and execute
`local-ci.sh` from the repository root:

```bash
bash local-ci.sh
```

The script runs pytest and generates a self-contained HTML report at
`reports/report.html`, creating the `reports/` directory if needed. Review the
report and resolve test failures before pushing.

To run the tests without generating an HTML report:

```bash
python -m pytest
```

Run these commands in the activated environment after installing the package
and `async-class`. The tests use MongoDB and Redis mocks and require no servers.
