from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

from ludic.base import BaseElement
from ludic.contrib.fastapi import LudicRoute
from ludic.html import div, p, span

app = FastAPI()
app.router.route_class = LudicRoute


@app.get("/component")
async def return_component() -> div:
    return div(span("Hello"), p("World"))


@app.get("/dict", response_model=None)
async def return_dict() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/custom-response")
async def return_custom_response() -> Response:
    return Response(content="Custom", media_type="text/plain")


@app.get("/nested")
async def nested_components() -> div:
    return div(p("Level 1", span("Level 2", div("Level 3"))), id="root")


@app.get("/f-string")
async def f_string_test() -> span:
    return span(f"Result: {p('This is a test')}")


@app.get("/status-code", status_code=202)
async def status_code_test() -> span:
    return span("this is a test")


def test_auto_component_conversion() -> None:
    client = TestClient(app)
    response = client.get("/component")

    assert response.status_code == 200
    assert response.content == b"<div><span>Hello</span><p>World</p></div>"
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_non_component_responses() -> None:
    client = TestClient(app)

    response = client.get("/dict")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

    response = client.get("/custom-response")
    assert response.status_code == 200
    assert response.content == b"Custom"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


def test_nested_components() -> None:
    client = TestClient(app)
    response = client.get("/nested")

    assert response.status_code == 200
    assert (
        b'<div id="root"><p>Level 1<span>Level 2<div>Level 3</div></span></p></div>'
        in response.content
    )


def test_formatter_cleanup_with_f_string() -> None:
    client = TestClient(app)
    response = client.get("/f-string")

    assert response.status_code == 200
    assert b"Result: <p>This is a test</p>" in response.content
    assert len(BaseElement.formatter.get()) == 0


def test_return_different_status_code() -> None:
    client = TestClient(app)
    response = client.get("/status-code")

    assert response.status_code == 202
