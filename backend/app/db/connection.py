import logging
import time
from functools import lru_cache

from arango import ArangoClient
from arango.database import StandardDatabase
from arango.exceptions import ArangoServerError, ServerConnectionError

from app.config import get_settings

log = logging.getLogger(__name__)


@lru_cache
def get_client() -> ArangoClient:
    return ArangoClient(hosts=get_settings().arango_url)


def wait_for_server(timeout_s: int = 60) -> None:
    """Block until ArangoDB answers. On `docker compose up` the backend
    usually starts before the database is ready, so we retry."""
    settings = get_settings()
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            sys_db = get_client().db("_system", username="root", password=settings.arango_root_password)
            version = sys_db.version()
            log.info("Connected to ArangoDB %s", version)
            return
        except (ServerConnectionError, ArangoServerError, ConnectionError) as exc:
            if time.monotonic() > deadline:
                raise RuntimeError(f"ArangoDB not reachable at {settings.arango_url}") from exc
            log.info("Waiting for ArangoDB...")
            time.sleep(2)


def ensure_database(name: str) -> StandardDatabase:
    """Create the database if it does not exist and return a handle to it."""
    settings = get_settings()
    client = get_client()
    sys_db = client.db("_system", username="root", password=settings.arango_root_password)
    if not sys_db.has_database(name):
        sys_db.create_database(name)
        log.info("Created database %s", name)
    return client.db(name, username="root", password=settings.arango_root_password)


def drop_database(name: str) -> None:
    settings = get_settings()
    sys_db = get_client().db("_system", username="root", password=settings.arango_root_password)
    if sys_db.has_database(name):
        sys_db.delete_database(name)


@lru_cache
def get_db() -> StandardDatabase:
    """FastAPI dependency: the application database.
    Used as `db: StandardDatabase = Depends(get_db)`, like @Autowired."""
    settings = get_settings()
    return get_client().db(settings.arango_db, username="root", password=settings.arango_root_password)
