from starlette.testclient import TestClient

from examples import app


def test_bulk_update() -> None:
    app.routes.clear()
    from examples.bulk_update import db

    with TestClient(app) as client:
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
    app.routes.clear()
    from examples.click_to_edit import db

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/contacts/1").status_code == 200
        assert client.get("/contacts/1/form/").status_code == 200
        assert client.get("/contacts/123").status_code == 404
        assert client.get("/contacts/123/form/").status_code == 404
        assert db.contacts["1"].first_name == "John"

        edit_data = {
            "first_name": "Test",
            "last_name": "Doe",
            "email": "test@example.com",
        }
        assert client.put("/contacts/1", data=edit_data).status_code == 200
        assert db.contacts["1"].first_name == "Test"


def test_click_to_load() -> None:
    app.routes.clear()
    import examples.click_to_load as _  # noqa

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/contacts/").status_code == 200
        assert client.get("/contacts/?page=2").status_code == 200


def test_delete_row() -> None:
    app.routes.clear()
    from examples.delete_row import db

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/people/").status_code == 200
        assert client.delete("/people/1").status_code == 200
        assert client.delete("/people/123").status_code == 404
        assert db.people.get("1") is None


def test_edit_row() -> None:
    app.routes.clear()
    from examples.edit_row import db

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/people/").status_code == 200
        assert client.get("/people/1").status_code == 200
        assert client.get("/people/1/form/").status_code == 200
        assert client.get("/people/123").status_code == 404
        assert client.get("/people/123/form/").status_code == 404

        assert db.people["1"].name == "Joe Smith"
        edit_data = {"name": "Test", "email": "test@example.com"}
        assert client.put("/people/1", data=edit_data).status_code == 200
        assert db.people["1"].name == "Test"
        assert db.people["1"].email == "test@example.com"
