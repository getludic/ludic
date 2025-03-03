from starlette.testclient import TestClient


def test_bulk_update() -> None:
    from examples.bulk_update import app, db

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
    from examples.click_to_edit import app, db

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
    from examples.click_to_load import app

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/contacts/").status_code == 200
        assert client.get("/contacts/?page=2").status_code == 200


def test_delete_row() -> None:
    from examples.delete_row import app, db

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/people/").status_code == 200
        assert client.delete("/people/1").status_code == 204
        assert client.delete("/people/123").status_code == 404
        assert db.people.get("1") is None


def test_edit_row() -> None:
    from examples.edit_row import app, db

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


def test_lazy_loading() -> None:
    from examples.lazy_loading import app

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        response = client.get("/load/0")
        assert response.status_code == 200
        assert b"Content Loaded" in response.content


def test_infinite_scroll() -> None:
    from examples.infinite_scroll import app

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/contacts/").status_code == 200
        assert client.get("/contacts/?page=2").status_code == 200


def test_fastapi_example() -> None:
    from examples.fastapi_example import app

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/cars/").status_code == 200
        assert client.get("/models/?manufacturer=audi").status_code == 200
        assert client.get("/models/").status_code == 404
