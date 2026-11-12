# Getting started

You need Docker with the Compose plugin and Git. Nothing else has to be installed on the host.

## Run the whole stack

```bash
git clone https://github.com/JovanVidovic96/auto-diag-kb.git
cd auto-diag-kb
cp .env.example .env        # then set passwords and JWT_SECRET
docker compose up --build
```

On the first start the backend waits for ArangoDB to become healthy, creates the `autodiag` database, all collections, graphs, indexes and the search view, and loads the seed data. Later starts skip the seed if the database already has data.

| Service | URL |
| --- | --- |
| Streamlit UI | http://localhost:8501 |
| FastAPI docs (Swagger) | http://localhost:8000/docs |
| ArangoDB web UI | http://localhost:8529 |

## First login

Log in with `ADMIN_USERNAME` and `ADMIN_PASSWORD` from `.env`. The seed also contains mechanic and owner accounts; their usernames are listed in `data/seed/users.json` and they all use the password from `SEED_USER_PASSWORD`.

## Reset the database

```bash
docker compose down -v      # removes the arangodb volume
docker compose up --build
```

## Rerun only the seed

```bash
docker compose run --rm backend python -m app.db.seed
```

The import uses `on_duplicate="replace"`, so it is safe to run more than once.
