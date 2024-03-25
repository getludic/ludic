from starlette.testclient import TestClient

from ludic.html import p
from ludic.web import LudicApp, Request
from ludic.web.exceptions import NotFoundError

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


def test_exceptions() -> None:
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
