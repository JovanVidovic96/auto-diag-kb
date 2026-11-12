# Configuration

All settings come from environment variables. Docker Compose reads them from `.env`. Only `.env.example` is committed. The backend loads them with `pydantic-settings` in `app/config.py`.

## Backend

| Variable | Example | Purpose |
| --- | --- | --- |
| `ARANGO_URL` | `http://arangodb:8529` | ArangoDB address inside the Compose network |
| `ARANGO_ROOT_PASSWORD` | `change-me` | Root password, also used by the ArangoDB container |
| `ARANGO_DB` | `autodiag` | Application database name |
| `JWT_SECRET` | long random string | Key for signing tokens (HS256) |
| `JWT_EXPIRE_MINUTES` | `60` | Token lifetime |
| `ADMIN_USERNAME` | `admin` | Admin account created on first start |
| `ADMIN_PASSWORD` | `change-me` | Password of that account |
| `SEED_USER_PASSWORD` | `demo1234` | Shared password of seeded mechanics and owners |
| `CORS_ORIGINS` | `http://localhost:8501` | Comma separated list of allowed origins |
| `LOG_LEVEL` | `INFO` | Python logging level |

## Frontend

| Variable | Example | Purpose |
| --- | --- | --- |
| `API_URL` | `http://backend:8000/api/v1` | Base URL of the backend |
| `DEFAULT_LANG` | `en` | Language shown before the user picks one |

## Ports

| Service | Port |
| --- | --- |
| arangodb | 8529 |
| backend | 8000 |
| frontend | 8501 |

## Tests

Tests use the same variables, but the database name is forced to `autodiag_test`. See [Testing](development/testing.md).
