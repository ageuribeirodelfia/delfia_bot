import pytest
from src.infra.database.settings.connection import DBConnectionHandler
from src.infra.repositories.incident_repository import IncidentRepository


@pytest.fixture(scope="module")
def db_connection():
    """Fixture para gerenciar a conexão com o banco de dados."""
    with DBConnectionHandler() as db_handler:
        db = db_handler.get_database()
        yield db  # Retorna o banco para ser usado nos testes


@pytest.mark.skip(reason="Sensive test")
def test_insert_incident(db_connection):
    title = 'any_title'
    description = 'any_description'
    status = 'any_status'

    incidents_repository = IncidentRepository()
    incidents_repository.insert_incident(title, description, status)

    result = db_connection["incidents"].find_one(
        {"title": title, "description": description, "status": status})

    assert result is not None
    assert result["title"] == title
    assert result["description"] == description
    assert result["status"] == status

    db_connection["incidents"].delete_one({"_id": result["_id"]})


@pytest.mark.skip(reason="Sensive test")
def test_select_incident(db_connection):
    title = 'any_title'
    description = 'any_description'
    status = 'any_status'

    db_connection["incidents"].insert_one(
        {"title": title, "description": description, "status": status})

    incidents_repository = IncidentRepository()
    incidents = incidents_repository.select_incident()

    assert len(incidents) > 0
    assert incidents[0]["title"] == title
    assert incidents[0]["description"] == description
    assert incidents[0]["status"] == status

    db_connection["incidents"].delete_one({"_id": incidents[0]["_id"]})
