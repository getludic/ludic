import asyncio
import inspect
from collections.abc import Generator
from typing import Any

import pytest
from starlette._utils import AwaitableOrContextManager, AwaitableOrContextManagerWrapper
from starlette.applications import Starlette
from starlette.datastructures import FormData, Headers, QueryParams
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

from ludic.base import BaseElement
from ludic.web.parsers import BaseParser
from ludic.web.responses import (
    LudicResponse,
    extract_from_request,
    extract_response_status_headers,
    prepare_response,
)


class DummyElement(BaseElement):
    def to_html(self) -> str:
        return "<p>Hello World</p>"


class DummyParser(BaseParser[Any]):
    def __init__(self, form: FormData) -> None:
        self.form = form


class DummyRequest(Request):
    path_params: dict[str, str] = {}
    query_params: QueryParams = QueryParams({"foo": "bar"})
    headers: Headers = Headers({"x": "y"})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def form(self, *args: Any, **kwargs: Any) -> AwaitableOrContextManager[FormData]:
        class DummyForm(FormData):
            async def __aenter__(self) -> Any:
                return self

            async def __aexit__(self, *a: Any) -> None:
                pass

            def __await__(self) -> Generator[None, None, FormData]:
                yield None
                return self

        return AwaitableOrContextManagerWrapper(DummyForm())


class DummyWebSocket(WebSocket):
    path_params: dict[str, str] = {}
    query_params: QueryParams = QueryParams({"foo": "bar"})
    headers: Headers = Headers({"x": "y"})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


def plain_handler() -> str:
    return "Hello"


def tuple_handler() -> tuple[str, int]:
    return "Hello", 201


def triple_handler() -> tuple[str, int, dict[str, str]]:
    return "Hello", 202, {"x-header": "yes"}


def invalid_tuple() -> tuple[str, int, dict[str, str], str]:
    return "Invalid", 201, {"x": "a"}, "extra"


def test_extract_response_status_headers_two_elements() -> None:
    body, code, headers = extract_response_status_headers(("hello", 404))
    assert isinstance(body, str)
    assert body == "hello"
    assert code == 404
    assert headers is None


def test_extract_response_status_headers_three_elements() -> None:
    _, _, headers = extract_response_status_headers(("hello", 200, {"x": "1"}))
    assert headers is not None and headers["x"] == "1"


def test_extract_response_status_headers_invalid_tuple() -> None:
    with pytest.raises(ValueError):
        extract_response_status_headers(("x", 1, {}, "extra"))


def test_ludic_response_render() -> None:
    response = LudicResponse(DummyElement())
    assert b"<p>Hello World</p>" in response.body


async def plain_view(request: Request) -> Response:
    return await prepare_response(lambda: "Hello plain", request)


async def tuple_view(request: Request) -> Response:
    return await prepare_response(lambda: ("Hi", 203), request)


async def element_view(request: Request) -> Response:
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


def test_extract_response_status_headers_invalid_length() -> None:
    with pytest.raises(ValueError):
        extract_response_status_headers(("a",))
    with pytest.raises(ValueError):
        extract_response_status_headers(("a", 1, {}, "extra"))


def test_prepare_response_invalid_type() -> None:
    async def handler() -> Any:
        return object()

    async def route_handler(req: Request) -> Response:
        return await prepare_response(handler, req)

    app = Starlette(routes=[Route("/invalid", route_handler)])
    client = TestClient(app)
    with pytest.raises(ValueError):
        client.get("/invalid")


def test_prepare_response_none() -> None:
    async def handler() -> None:
        return None

    async def route_handler(req: Request) -> Response:
        return await prepare_response(handler, req)

    app = Starlette(routes=[Route("/none", route_handler)])
    client = TestClient(app)
    resp = client.get("/none")
    assert resp.status_code == 204


def test_extract_from_request_issubclass_typeerror() -> None:
    def handler(x: int) -> int:
        return x

    param = list(inspect.signature(handler).parameters.values())[0]
    param = param.replace(annotation=123)
    result = asyncio.run(extract_from_request(lambda x: x, DummyRequest()))

    assert isinstance(result, dict)


def test_extract_from_request_invalid_union() -> None:
    def handler(x: int | str) -> int | str:
        return x

    with pytest.raises(TypeError):
        asyncio.run(extract_from_request(handler, DummyRequest()))


def test_extract_from_request_empty_annotation() -> None:
    def handler(x: Any) -> Any:
        return x

    result = asyncio.run(extract_from_request(handler, DummyRequest()))
    assert isinstance(result, dict)


def test_extract_from_request_unknown_type() -> None:
    class Unknown:
        pass

    def handler(x: Unknown) -> Unknown:
        return x

    result = asyncio.run(extract_from_request(handler, DummyRequest()))
    assert isinstance(result, dict)


def test_extract_from_request_all_types() -> None:
    def handler(
        ws: WebSocket,
        parser: DummyParser,
        form: FormData,
        req: Request,
        qp: QueryParams,
        hdr: Headers,
    ) -> None:
        return None

    request = DummyRequest()
    request.__class__.__name__ = "WebSocket"
    result = asyncio.run(extract_from_request(handler, request))
    assert set(result.keys()) == {"form", "req", "qp", "hdr"}

    websocket_request = DummyWebSocket()
    websocket_result = asyncio.run(extract_from_request(handler, websocket_request))
    assert set(websocket_result.keys()) == {"ws"}


def test_prepare_response_handler_exception() -> None:
    def handler() -> None:
        raise RuntimeError("fail")

    async def route_handler(req: Request) -> Response:
        return await prepare_response(handler, req)

    app = Starlette(routes=[Route("/fail", route_handler)])
    client = TestClient(app)

    with pytest.raises(RuntimeError):
        client.get("/fail")
