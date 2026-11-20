from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_is_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["version"] == "dev"  # no GIT_SHA outside a CI-built image


def test_create_and_list_note():
    r = client.post("/notes", json={"title": "Hi", "content": "First note"})
    assert r.status_code == 201
    created = r.json()
    assert created["title"] == "Hi"
    assert created["id"] == 1

    assert client.get("/notes").json() == [created]


def test_notes_are_stored_in_the_database():
    from sqlalchemy import text

    from app.db import get_engine

    client.post("/notes", json={"title": "Saved", "content": "In Postgres"})
    with get_engine().connect() as conn:
        title = conn.execute(text("SELECT title FROM notes")).scalar_one()
    assert title == "Saved"


def test_empty_title_is_rejected():
    r = client.post("/notes", json={"title": "", "content": "x"})
    assert r.status_code == 422
