import inspect
from collections.abc import Callable
from typing import Any, Literal

from starlette._utils import is_async_callable
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.routing import get_name
from starlette.types import Receive, Scope, Send

from ..elements.base import Element
from .endpoints import PyMXEndpoint
from .response import PyMXResponse


class _PyMXHandler:
    def __init__(self, handler: Callable[..., Any]) -> None:
        self.handler = handler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive)
        is_async = is_async_callable(self.handler)
        if is_async:
            response = await self.handler(request)
        else:
            response = await run_in_threadpool(self.handler, request)
        if isinstance(response, Element):
            response = PyMXResponse(response)
        await response(scope, receive, send)


class PyMXApp(Starlette):
    """Starlette application with PyMX methods.

    Example:

        async def homepage(request: Request) -> html:
            return html(...)

        app = PyMXApp(debug=True)
        app.add_pymx_route("/", homepage)

    You can also use a method decorator to register a PyMX endpoint:

        @app.get("/")
        async def homepage(request: Request) -> button:
            return button(...)
    """

    def get(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register GET endpoint to the application."""
        return self.register_pymx_route(path, method="GET", **kwargs)

    def post(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register POST endpoint to the application."""
        return self.register_pymx_route(path, method="POST", **kwargs)

    def put(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register PUT endpoint to the application."""
        return self.register_pymx_route(path, method="PUT", **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register DELETE endpoint to the application."""
        return self.register_pymx_route(path, method="DELETE", **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register PATCH endpoint to the application."""
        return self.register_pymx_route(path, method="PATCH", **kwargs)

    def register_pymx_route(
        self,
        path: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = "GET",
        include_in_schema: bool = True,
    ) -> Callable[..., Any]:
        """Register an endpoint to the application."""

        def register(handler: Callable[..., Any]) -> Callable[..., Any]:
            self.add_pymx_route(
                path, handler, methods=[method], include_in_schema=include_in_schema
            )
            return handler

        return register

    def endpoint(
        self,
        path: str,
        include_in_schema: bool = True,
    ) -> Callable[..., Any]:
        """Register a PyMX class endpoint to the application."""

        def register(endpoint: type[PyMXEndpoint]) -> type[PyMXEndpoint]:
            self.add_pymx_route(path, endpoint, include_in_schema=include_in_schema)
            return endpoint

        return register

    def add_pymx_route(
        self,
        path: str,
        handler: Callable[..., Any],
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Add a PyMX endpoint to the application.

        The endpoint will be wrapped in a :class:`~pymx.starlette.response.PyMXResponse`
        if a PyMX component is returned. This means that it is possible to return
        a PyMX component instance from the handler directly instead of wrapping it
        in the :class:`~pymx.starlette.response.PyMXResponse`.

        It is still possible to return a regular response from the handler
        (e.g. ``JSONResponse({"hello": "world"})``).
        """
        if inspect.isfunction(handler) or inspect.ismethod(handler):
            name = get_name(handler) if name is None else name
            handler = _PyMXHandler(handler)
        super().add_route(path, handler, name=name, **kwargs)
