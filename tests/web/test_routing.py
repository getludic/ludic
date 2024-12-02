import pytest
from starlette.testclient import TestClient

from ludic.html import div
from ludic.web import LudicApp
from ludic.web.datastructures import Headers

app = LudicApp()


@app.get("/mandatory-param/{test}")
def mandatory_param(test: str) -> div:
    return div(test)


@app.get("/extract-headers/")
def extract_headers(headers: Headers) -> div:
    return div(headers["X-Foo"])


@app.get("/kw-only-params")
def kw_only_params(*, bar: str | None) -> div:
    return div(bar or "nothing")


@app.get("/invalid-signature")
def invalid_signature(*, bar: str | int) -> div:
    return div(bar or "nothing")


def test_mandatory_param() -> None:
    with TestClient(app) as client:
        response = client.get("/mandatory-param/value")
        assert response.content.decode("utf-8") == "<div>value</div>"


def test_extract_headers() -> None:
    with TestClient(app) as client:
        response = client.get("/extract-headers", headers={"X-Foo": "x-foo-value"})
        assert response.content.decode("utf-8") == "<div>x-foo-value</div>"


def test_kw_only_params() -> None:
    with TestClient(app) as client:
        response = client.get("/kw-only-params?bar=something")
        assert response.content.decode("utf-8") == "<div>something</div>"
        response = client.get("/kw-only-params")
        assert response.content.decode("utf-8") == "<div>nothing</div>"


def test_invalid_signature() -> None:
    with TestClient(app) as client, pytest.raises(TypeError):
        client.get("/invalid-signature?bar=something")
