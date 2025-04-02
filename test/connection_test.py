import pytest
from pymongo import MongoClient
from src.infra.database.settings.connection import DBConnectionHandler


@pytest.mark.skip(reason="Sensive Test")
def test_create_database_connection():
    db_connection_handle = DBConnectionHandler()
    database = db_connection_handle.get_database()

    assert database is not None
    assert isinstance(database, MongoClient().get_database().__class__)


def test_connect():
    db_connection_handler = DBConnectionHandler()
    database_name = "rpa_telmex_db"
    database = db_connection_handler.connect(database_name)

    assert database.name == database_name

def test_close_connection():
    db_connection_handler = DBConnectionHandler()
    db_connection_handler.close_connection()

    assert db_connection_handler is not None

def test_with_statement():
    with DBConnectionHandler() as db_handler:
        database = db_handler.get_database()
        assert database is not None