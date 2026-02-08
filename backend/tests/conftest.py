import pytest
import os
import sys
import sqlite3

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"))

from database.connection import get_db_connection, init_db, DB_PATH

TEST_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "test_school_calendar.db")


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Use separate test DB to avoid polluting real data."""
    import database.connection as conn_module
    conn_module.DB_PATH = TEST_DB_PATH
    os.makedirs(os.path.dirname(TEST_DB_PATH), exist_ok=True)
    init_db()
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
def db_conn():
    import database.connection as conn_module
    conn_module.DB_PATH = TEST_DB_PATH
    conn = get_db_connection()
    yield conn
    conn.close()


@pytest.fixture
def clean_db(db_conn):
    """Clean all data before test."""
    db_conn.execute("DELETE FROM events")
    db_conn.execute("DELETE FROM schools")
    db_conn.commit()
    return db_conn
