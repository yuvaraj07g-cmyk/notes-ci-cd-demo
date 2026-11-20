import os

import pytest
from dotenv import load_dotenv

load_dotenv()  # lets you keep TEST_DATABASE_URL in your local .env

# Tests ALWAYS use a separate test database, never your real one,
# because every test starts by emptying the notes table.
_test_url = os.getenv("TEST_DATABASE_URL")
if not _test_url:
    pytest.exit(
        "TEST_DATABASE_URL is not set. Create a 'test' branch in Neon, "
        "copy its connection string and add it to your .env file.",
        returncode=2,
    )
if _test_url == os.getenv("DATABASE_URL"):
    pytest.exit(
        "TEST_DATABASE_URL must be a DIFFERENT database from DATABASE_URL. "
        "Tests empty the notes table.",
        returncode=2,
    )
os.environ["DATABASE_URL"] = _test_url


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    from app.db import Base, get_engine

    Base.metadata.create_all(get_engine())


@pytest.fixture(autouse=True)
def _empty_notes_table():
    from sqlalchemy import text

    from app.db import get_engine

    with get_engine().begin() as conn:
        conn.execute(text("TRUNCATE notes RESTART IDENTITY"))
