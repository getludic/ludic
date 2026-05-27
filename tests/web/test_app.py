import pytest
from starlette.testclient import TestClient

from ludic.html import div
from ludic.web import LudicApp


def test_lifespan_kwarg_is_supported() -> None:
    state: dict[str, bool] = {"started": False, "stopped": False}

    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(app):  # type: ignore[no-untyped-def]
        state["started"] = True
        yield
        state["stopped"] = True

    app = LudicApp(lifespan=lifespan)

    @app.get("/")
    def index() -> div:
        return div("ok")

    with TestClient(app) as client:
        assert state["started"] is True
        assert client.get("/").status_code == 200
    assert state["stopped"] is True


def test_on_startup_and_on_shutdown_emit_deprecation_and_still_run() -> None:
    calls: list[str] = []

    def startup() -> None:
        calls.append("startup")

    async def shutdown() -> None:
        calls.append("shutdown")

    with pytest.warns(DeprecationWarning, match="on_startup"):
        app = LudicApp(on_startup=[startup], on_shutdown=[shutdown])

    @app.get("/")
    def index() -> div:
        return div("ok")

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert calls == ["startup"]
    assert calls == ["startup", "shutdown"]


def test_lifespan_and_on_startup_cannot_be_combined() -> None:
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(app):  # type: ignore[no-untyped-def]
        yield

    with pytest.raises(AssertionError):
        LudicApp(on_startup=[lambda: None], lifespan=lifespan)
