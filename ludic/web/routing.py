import inspect
from collections.abc import Callable
from typing import Any

from starlette import routing
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Host
from starlette.types import Receive, Scope, Send

from ludic.attrs import Attrs

from .endpoints import Endpoint
from .requests import Request
from .responses import prepare_response

__all__ = (
    "Host",
    "Mount",
    "Route",
    "Router",
)


class Mount(routing.Mount):
    """Mount class for Ludic components."""

    def matches(self, scope: Scope) -> tuple[routing.Match, Scope]:
        match, scope = super().matches(scope)
        if match == routing.Match.FULL:
            if partial := scope.get("partial_mount"):
                scope["partial_mount"] = f"{partial}:{self.name}"
            else:
                scope["partial_mount"] = self.name
        return match, scope


class _FunctionHandler:
    def __init__(self, handler: Callable[..., Any]) -> None:
        self.handler = handler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive)
        response = await prepare_response(self.handler, request)
        await response(scope, receive, send)


class _EndpointHandler:
    def __init__(self, handler: type[Endpoint[Attrs]]) -> None:
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
        response = await prepare_response(handler, request)
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


class Route(routing.Route):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        name = routing.get_name(endpoint) if name is None else name
        wrapped_route = endpoint
        if inspect.isfunction(endpoint) or inspect.ismethod(endpoint):
            wrapped_route = _FunctionHandler(endpoint)
        elif inspect.isclass(endpoint) and issubclass(endpoint, Endpoint):
            wrapped_route = _EndpointHandler(endpoint)
        if getattr(endpoint, "route", None) is None:
            endpoint.route = self  # type: ignore
        super().__init__(path, wrapped_route, name=name, **kwargs)


class Router(routing.Router):
    def add_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> None:
        route = Route(
            path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
