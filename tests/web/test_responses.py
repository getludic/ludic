# tests/web/test_responses.py
import pytest
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.testclient import TestClient
from starlette.responses import Response

from ludic.web.responses import (
    BaseElement,
    LudicResponse,
    extract_response_status_headers,
    prepare_response,
)


# Dummy BaseElement subclass for testing
class DummyElement(BaseElement):
    def to_html(self) -> str:
        return "<p>Hello World</p>"


# Dummy handler functions
def plain_handler() -> str:
    return "Hello"


def tuple_handler() -> tuple[str, int]:
    return "Hello", 201


def triple_handler() -> tuple[str, int, dict[str, str]]:
    return "Hello", 202, {"x-header": "yes"}


def invalid_tuple() -> tuple[str, int, dict[str, str], str]:
    return "Invalid", 201, {"x": "a"}, "extra"


# ---------- UNIT TESTS ---------- #


def test_extract_response_status_headers_two_elements() -> None:
    r, code, headers = extract_response_status_headers(("hello", 404))
    assert r[0] == "hello"
    assert code == 404
    assert headers is None


def test_extract_response_status_headers_three_elements() -> None:
    r, code, headers = extract_response_status_headers(("hello", 200, {"x": "1"}))
    assert headers is not None and headers["x"] == "1"


def test_extract_response_status_headers_invalid_tuple() -> None:
    with pytest.raises(ValueError):
        extract_response_status_headers(("x", 1, {}, "extra"))


def test_ludic_response_render() -> None:
    response = LudicResponse(DummyElement())
    assert b"<p>Hello World</p>" in response.body


# ---------- INTEGRATION TEST ---------- #


async def plain_view(request) -> Response:
    return await prepare_response(lambda: "Hello plain", request)


async def tuple_view(request) -> Response:
    return await prepare_response(lambda: ("Hi", 203), request)


async def element_view(request) -> Response:
    return await prepare_response(lambda: DummyElement(), request)


app = Starlette(
    routes=[
        Route("/plain", plain_view),
        Route("/tuple", tuple_view),
        Route("/element", element_view),
    ]
)

client = TestClient(app)


def test_prepare_response_plaintext() -> None:
    response = client.get("/plain")
    assert response.status_code == 200
    assert response.text == "Hello plain"


def test_prepare_response_tuple() -> None:
    response = client.get("/tuple")
    assert response.status_code == 203
    assert response.text == "Hi"


def test_prepare_response_ludic_element() -> None:
    response = client.get("/element")
    assert response.status_code == 200
    assert "<p>Hello World</p>" in response.text
