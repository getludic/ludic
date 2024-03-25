import pytest
from starlette.testclient import TestClient

from ludic.html import p
from ludic.web import LudicApp, Request
from ludic.web.exceptions import (
    BadGatewayError,
    BadRequestError,
    ClientError,
    ForbiddenError,
    GatewayTimeoutError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
    NotImplementedError,
    PaymentRequiredError,
    ServerError,
    ServiceUnavailableError,
    TooManyRequestsError,
    UnauthorizedError,
)

app = LudicApp()


@app.get("/")
async def index() -> p:
    return p("hello world")


@app.get("/error")
async def error() -> p:
    raise RuntimeError("error happened")


@app.post("/only-post")
async def only_post() -> p:
    return p("only post")


@app.get("/not-found")
async def page_not_found() -> p:
    raise NotFoundError("This page does not exist.")


@app.exception_handler(404)
async def not_found(request: Request) -> p:
    return p(f"page {request.url.path} does not exist")


@app.exception_handler(405)
async def method_not_allowed() -> p:
    return p("method not allowed")


@app.exception_handler(500)
async def server_error(exception: Exception) -> p:
    return p(f"server error: {exception}")


def test_exception_handling() -> None:
    test_data = [
        ("/", 200, "hello world"),
        ("/not-found", 404, "page /not-found does not exist"),
        ("/only-post", 405, "method not allowed"),
        ("/error", 500, "server error: error happened"),
    ]

    with TestClient(app, raise_server_exceptions=False) as client:
        for path, status, content in test_data:
            response = client.get(path)
            assert response.status_code == status
            assert response.text == p(content).to_html()


def test_exceptions() -> None:
    test_data = [
        (ClientError, 400),
        (BadRequestError, 400),
        (UnauthorizedError, 401),
        (PaymentRequiredError, 402),
        (ForbiddenError, 403),
        (NotFoundError, 404),
        (MethodNotAllowedError, 405),
        (TooManyRequestsError, 429),
        (ServerError, 500),
        (InternalServerError, 500),
        (NotImplementedError, 501),
        (BadGatewayError, 502),
        (ServiceUnavailableError, 503),
        (GatewayTimeoutError, 504),
    ]

    for Error, status_code in test_data:
        assert issubclass(Error, Exception)
        with pytest.raises(Error) as error:
            raise Error("test message")

        assert (
            error.exconly()
            == f"ludic.web.exceptions.{Error.__name__}: {status_code}: test message"
        )
