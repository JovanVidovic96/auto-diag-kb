# Local development

Development happens on Ubuntu with the Zed editor. The database runs in Docker; backend and frontend can run in Docker or directly from a virtual environment, which is faster for editing.

## Database only in Docker

```bash
docker compose up -d arangodb
```

## Backend from a venv

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' ../.env | xargs)
export ARANGO_URL=http://localhost:8529
python -m app.db.seed          # first time only
uvicorn app.main:app --reload --port 8000
```

`--reload` restarts the server on every saved file.

## Frontend from a venv

```bash
cd frontend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
API_URL=http://localhost:8000/api/v1 streamlit run Home.py
```

## Docs

```bash
pip install mkdocs pymdown-extensions
mkdocs serve                   # http://localhost:8000, stop the backend first or use -a localhost:8001
```

## Useful habits

- Write and test a query in the ArangoDB web UI (Queries tab) first, then copy it into `app/queries/`.
- Keep AQL out of Python strings. If a query needs to change, change the `.aql` file.
- Run `pytest` before every commit.
- Formatting and linting with `ruff format` and `ruff check`.

## Python notes for a Java developer

| Java / Spring | Here |
| --- | --- |
| Maven `pom.xml` | `requirements.txt` + `venv` |
| `@RestController` + `@PostMapping` | `router = APIRouter()` + `@router.post(...)` |
| DTO with `@NotNull`, `@Size` | Pydantic `BaseModel` with `Field(min_length=...)` |
| `@Autowired` | `Depends(...)` |
| `Optional<T>` | `T \| None` |
| JUnit + MockMvc | pytest + `TestClient` |
| `application.properties` | `.env` + `pydantic-settings` |
