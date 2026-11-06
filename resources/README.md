# Local CI `absp`

Pull Redis image from registry : 

```bash
docker pull ghcr.io/variton/iredis:1.0
```


Move the `docker-compose.yml` file to the project root directory.

## Direct execution

```bash
docker compose run --rm absp local-ci.sh
```

## Interactive execution (inside the container)

```bash
docker compose up -d
docker compose exec absp bash
local-ci.sh
```

## Shutdown

```bash
docker compose down
```

## Reports

Test reports are generated in the `reports/` directory :

- `unit-tests.html`
- `integration-tests.html`
- `coverage/index.html`
