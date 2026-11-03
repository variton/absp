# Local CI `absp`

Pull Redis image from regisrtry : 

```bash
docker pull ghcr.io/variton/redis:8.6-alpine 
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
