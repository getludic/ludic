import inspect
from collections.abc import Callable
from typing import Any

from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Host, Mount, get_name
from starlette.routing import (
    Route as StarletteRoute,
)
from starlette.routing import (
    Router as StarletteRouter,
)
from starlette.types import Receive, Scope, Send

from .datastructures import URLPath
from .endpoints import Endpoint
from .requests import Request
from .responses import prepare_response

__all__ = (
    "Host",
    "Mount",
    "Route",
    "Router",
)


class _FunctionHandler:
    def __init__(self, handler: Callable[..., Any]) -> None:
        self.handler = handler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive)
        response = await prepare_response(self.handler, request)
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


class Route(StarletteRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        name = get_name(endpoint) if name is None else name
        wrapped_route = endpoint
        if inspect.isfunction(endpoint) or inspect.ismethod(endpoint):
            wrapped_route = _FunctionHandler(endpoint)
        elif inspect.isclass(endpoint) and issubclass(endpoint, Endpoint):
            wrapped_route = _EndpointHandler(endpoint)
        if getattr(endpoint, "route", None) is None:
            endpoint.route = self  # type: ignore
        super().__init__(path, wrapped_route, name=name, **kwargs)

    def url_path_for(self, name: str, /, **path_params: Any) -> URLPath:
        result = super().url_path_for(name, **path_params)
        return URLPath(result, result.protocol, result.host)


class Router(StarletteRouter):
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

    def url_path_for(self, name: str, /, **path_params: Any) -> URLPath:
        return super().url_path_for(name, **path_params)  # type: ignore
