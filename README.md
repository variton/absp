# Asynchronous Backend Store Package (ABSP)

A Python package under development for asynchronous backend storage.

## Overview

ABSP aims to provide asynchronous backend storage functionality through the
`absp` Python package, with subpackages for data lakes, databases, and in-memory
storage.

## Project Status

The package currently provides asynchronous store factories (`IAbsp` and `IDb`)
and a MongoDB mock (`AMongoDbMock`). The mock prints connection information and
returns `True` from `connect()`; it does not connect to a database or implement
data persistence.

Only MongoDB is mapped to an implementation. PostgreSQL and SQLite have enum
values but no implementations, and the `datalake` and `inmemory` subpackages
remain skeletons. Two asynchronous tests exercise the MongoDB mock through the
store and database factories.

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
required. You can also create it with
`await IDb().get(EDb.MGDB, url, database_name)`, importing `IDb` from
`absp.db.idb` and `EDb` from `absp.db.edb`. Unsupported store names or unmapped
database enum values raise `KeyError`.

## Repository Layout

```text
pyproject.toml       Package metadata, dependencies, and build configuration
local-ci.sh         Local test execution and HTML report generation
src/absp/           Main Python package
    iabsp.py        Asynchronous store factory ("mongo")
    datalake/       Data lake package skeleton
    db/             Database factory, backend enum, mapper, and MongoDB mock
    inmemory/       In-memory storage package skeleton
tests/              Asynchronous factory and mock connection tests
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
and `async-class`. The tests use the MongoDB mock and require no database server.
