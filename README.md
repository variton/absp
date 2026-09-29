# Asynchronous Backend Store Package (ABSP)

A Python package under development for asynchronous backend storage.

## Overview

ABSP aims to provide asynchronous backend storage functionality through the
`absp` Python package, with subpackages for data lakes, databases, and in-memory
storage.

## Project Status

This repository currently contains package metadata and a source package
skeleton. The `datalake`, `db`, and `inmemory` subpackages contain only package
docstrings; storage implementations and public APIs are not yet available.
The `tests/` directory is currently empty.

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
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in
PowerShell instead.

The project currently declares development, testing, linting, security, and
documentation tools as package dependencies, so installation includes those
tools.

Verify that the package can be imported:

```bash
python -c "import absp; print(absp.__file__)"
```

## Repository Layout

```text
pyproject.toml       Package metadata, dependencies, and build configuration
src/absp/           Main Python package
    datalake/       Data lake package skeleton
    db/             Database package skeleton
    inmemory/       In-memory storage package skeleton
tests/              Directory for future tests
```

## Development

Once tests are added, run them from the repository root with:

```bash
python -m pytest
```

With the current empty test directory, pytest reports no tests collected and
exits with code 5.

Usage examples and API documentation will be added as storage implementations
become available.
