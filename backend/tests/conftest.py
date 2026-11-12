import pytest

from app.db.connection import drop_database, ensure_database, wait_for_server
from app.db.schema import ensure_schema

TEST_DB = "autodiag_test"


@pytest.fixture(scope="session")
def db():
    """A fresh test database with the full schema, dropped after the test run.
    The application database (autodiag) is never touched."""
    wait_for_server()
    drop_database(TEST_DB)
    database = ensure_database(TEST_DB)
    ensure_schema(database)
    yield database
    drop_database(TEST_DB)
