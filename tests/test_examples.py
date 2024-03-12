from starlette.testclient import TestClient

from examples import app, db


def test_bulk_update() -> None:
    import examples.bulk_update as _  # noqa

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/people/").status_code == 200
    assert db.people["1"].active
    assert db.people["2"].active
    assert db.people["3"].active
    assert not db.people["4"].active

    activate_data = {"active:id:1": "on", "active:id:2": "on"}
    assert client.post("/people/", data=activate_data).status_code == 200
    assert db.people["1"].active
    assert db.people["2"].active
    assert not db.people["3"].active
    assert not db.people["4"].active


def test_click_to_edit() -> None:
    import examples.click_to_edit as _  # noqa

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/contacts/1").status_code == 200
    assert client.get("/contacts/1/form/").status_code == 200
    assert client.get("/contacts/123").status_code == 404
    assert client.get("/contacts/123/form/").status_code == 404
    assert db.contacts["1"].first_name == "John"

    edit_data = {"first_name": "Test", "last_name": "Doe", "email": "test@example.com"}
    assert client.put("/contacts/1", data=edit_data).status_code == 200
    assert db.contacts["1"].first_name == "Test"


def test_click_to_load() -> None:
    import examples.click_to_load as _  # noqa

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/contacts/").status_code == 200
    assert client.get("/contacts/?page=2").status_code == 200


def test_delete_row() -> None:
    import examples.delete_row as _  # noqa

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/people/").status_code == 200
    assert client.delete("/people/1").status_code == 200
    assert client.delete("/people/123").status_code == 404


def test_edit_row() -> None:
    import examples.edit_row as _  # noqa

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/contacts/").status_code == 200
    assert client.get("/contacts/1").status_code == 200
    assert client.get("/contacts/1/form/").status_code == 200
    assert client.get("/contacts/123").status_code == 404
    assert client.get("/contacts/123/form/").status_code == 404
