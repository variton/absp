# absp

**Asynchronous Backend Store Package** — a Python package for creating storage
adapters through a shared asynchronous factory.

## Storage adapters

`IAbsp.get(name, *args)` creates an adapter; call its asynchronous `connect()`
method separately. Import the factory from `absp.iabsp`.

| Factory name | Adapter | Constructor arguments |
| --- | --- | --- |
| `redis` | Redis client (`redis.asyncio`) | Host, port, optional response decoding flag (default: `True`) |
| `rmock` | Redis mock | Optional host and port |
| `mongo` | MongoDB mock | Server URL and database name |
| `s3` | S3 mock | Bucket name |

MongoDB and S3 currently use mock implementations. Adapter operations are still
under development; some methods are placeholders.

## Local setup

Requirements:

- Python 3.14 or newer.
- [uv](https://docs.astral.sh/uv/) and Git. The `xphide` dependency is installed
  from its Git repository at tag `v0.1.1`.
- Redis on `localhost:6379` for tests that exercise the Redis adapter.
- Docker with Docker Compose for the container workflow below.

From the repository root, install the package and development dependencies:

```bash
uv sync
```

## Tests and local CI

Run individual test suites from the repository root:

```bash
uv run pytest tests -v
uv run pytest nrtests -v
```

Both suites include tests using the Redis adapter, so keep a Redis service
available on `localhost:6379`.

Run the complete local CI pipeline:

```bash
uv run bash ./local-ci.sh
```

The script synchronizes dependencies, checks formatting with Black, runs the unit
and integration suites, and generates combined coverage. It stops at the first
failed step and replaces the `reports/` directory on each run.

### Run CI in Docker

Copy the Compose configuration to the repository root so its bind mount points
at the project:

```bash
cp resources/docker-compose.yml docker-compose.yml
docker compose pull
docker compose run --rm absp uv run bash ./local-ci.sh
```

The configuration uses `redis:8.6-alpine` and `ghcr.io/variton/iabsp:1.0`.
Compose starts Redis and waits for its health check before starting `absp`.
The containers share a network namespace, making Redis available to the tests
at `localhost:6379`. Port 6379 must be available on the host.

For an interactive session:

```bash
docker compose up -d
docker compose exec absp bash
uv run bash ./local-ci.sh
exit
```

Shut down the services:

```bash
docker compose down
```

### Reports

After a successful CI run, open these files in `reports/`:

- `unit-tests.html` — unit test results.
- `integration-tests.html` — integration test results.
- `coverage/index.html` — combined HTML coverage report.

## Repository layout

- `src/absp/` — storage factory, interfaces, and adapters.
- `tests/` — unit tests, including Redis operations.
- `nrtests/` — sequential and concurrent multi-store integration tests.
- `resources/` — Docker Compose configuration and container instructions.
- `local-ci.sh` — formatting, tests, and coverage pipeline.
