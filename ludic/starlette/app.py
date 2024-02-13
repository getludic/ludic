import inspect
from collections.abc import Callable
from typing import Any, Literal, cast

from starlette._utils import is_async_callable
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route, get_name
from starlette.types import Receive, Scope, Send

from ludic.base import Element

from .endpoints import Endpoint
from .response import LudicResponse


class _FunctionHandler:
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
            response = LudicResponse(response)
        await response(scope, receive, send)


class _EndpointHandler:
    def __init__(self, handler: type[Endpoint]) -> None:
        self.handler = handler
        self._allowed_methods = [
            method
            for method in ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
            if getattr(self.handler, method.lower(), None) is not None
        ]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive)
        handler_name = (
            "get"
            if request.method == "HEAD" and not hasattr(self, "head")
            else request.method.lower()
        )
        handler: Callable[..., Any] = getattr(
            self.handler, handler_name, self.method_not_allowed(scope)
        )

        handler_kwargs: dict[str, Any] = {}
        parameters = inspect.signature(handler).parameters

        if all(key in parameters for key in request.path_params):
            handler_kwargs.update(request.path_params)

        for name, param in parameters.items():
            if issubclass(param.annotation, FormData):
                async with request.form() as form:
                    handler_kwargs[name] = form
            if issubclass(param.annotation, Request):
                handler_kwargs[name] = request

        is_async = is_async_callable(handler)
        if is_async:
            response = await handler(**handler_kwargs)
        else:
            response = await run_in_threadpool(handler, **handler_kwargs)
        if isinstance(response, Element):
            response = LudicResponse(response)
        await response(scope, receive, send)

    def method_not_allowed(self, scope: Scope) -> Callable[..., Any]:
        # If we're running inside a starlette application then raise an
        # exception, so that the configurable exception handler can deal with
        # returning the response. For plain ASGI apps, just return the response.
        headers = {"Allow": ", ".join(self._allowed_methods)}

        async def make_response(request: Request) -> Response:
            if "app" in scope:
                raise HTTPException(status_code=405, headers=headers)
            return PlainTextResponse(
                "Method Not Allowed", status_code=405, headers=headers
            )

        return make_response


class LudicApp(Starlette):
    """Starlette application with Ludic methods.

    Example:

        async def homepage(request: Request) -> html:
            return html(...)

        app = LudicApp(debug=True)
        app.add_route("/", homepage)

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
            self.add_route(
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

        def register(endpoint: type[Endpoint]) -> type[Endpoint]:
            self.add_route(path, endpoint, include_in_schema=include_in_schema)
            endpoint.route = cast(Route, self.router.routes[-1])
            return endpoint

        return register

    def add_route(
        self,
        path: str,
        route: Callable[..., Any],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> None:
        """Add a PyMX endpoint to the application.

        The endpoint will be wrapped in a :class:`~pymx.starlette.response.PyMXResponse`
        if a PyMX component is returned. This means that it is possible to return
        a PyMX component instance from the handler directly instead of wrapping it
        in the :class:`~pymx.starlette.response.PyMXResponse`.

        It is still possible to return a regular response from the handler
        (e.g. ``JSONResponse({"hello": "world"})``).
        """
        name = get_name(route) if name is None else name
        if inspect.isfunction(route) or inspect.ismethod(route):
            route = _FunctionHandler(route)
        elif inspect.isclass(route) and issubclass(route, Endpoint):
            route = _EndpointHandler(route)
        super().add_route(
            path,
            route,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
