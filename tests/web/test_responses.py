# tests/web/test_responses.py
from ludic.web import responses
import pytest
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from starlette.testclient import TestClient
from starlette.routing import Route
from ludic.web.responses import (
    extract_response_status_headers,
    prepare_response,
    LudicResponse,
    BaseElement,
)

from starlette.applications import Starlette


# Dummy BaseElement subclass for testing
class DummyElement(BaseElement):
    def to_html(self):
        return "<p>Hello World</p>"


# Dummy handler functions
def plain_handler():
    return "Hello"

def tuple_handler():
    return "Hello", 201

def triple_handler():
    return "Hello", 202, {"x-header": "yes"}

def invalid_tuple():
    return "Invalid", 201, {"x": "a"}, "extra"


# ---------- UNIT TESTS ---------- #

def test_extract_response_status_headers_two_elements():
    r, code, headers = extract_response_status_headers(("hello", 404))
    assert r == "hello"
    assert code == 404
    assert headers is None

def test_extract_response_status_headers_three_elements():
    r, code, headers = extract_response_status_headers(("hello", 200, {"x": "1"}))
    assert r == "hello"
    assert code == 200
    assert headers["x"] == "1"

def test_extract_response_status_headers_invalid_tuple():
    with pytest.raises(ValueError):
        extract_response_status_headers(("x", 1, {}, "extra"))


def test_ludic_response_render():
    response = LudicResponse(DummyElement())
    assert b"<p>Hello World</p>" in response.body


# ---------- INTEGRATION TEST ---------- #

async def plain_view(request):
    return await prepare_response(lambda: "Hello plain", request)

async def tuple_view(request):
    return await prepare_response(lambda: ("Hi", 203), request)

async def element_view(request):
    return await prepare_response(lambda: DummyElement(), request)

app = Starlette(
    routes=[
        Route("/plain", plain_view),
        Route("/tuple", tuple_view),
        Route("/element", element_view),
    ]
)

client = TestClient(app)

def test_prepare_response_plaintext():
    response = client.get("/plain")
    assert response.status_code == 200
    assert response.text == "Hello plain"

def test_prepare_response_tuple():
    response = client.get("/tuple")
    assert response.status_code == 203
    assert response.text == "Hi"

def test_prepare_response_ludic_element():
    response = client.get("/element")
    assert response.status_code == 200
    assert "<p>Hello World</p>" in response.text
