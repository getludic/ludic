import inspect
from collections.abc import Callable, Mapping, Sequence
from functools import wraps
from typing import Any, Literal, TypeVar, cast

from starlette._utils import is_async_callable
from starlette.applications import AppType, Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan
from starlette.websockets import WebSocket

from ludic.attrs import Attrs
from ludic.base import BaseElement

from .datastructures import URLPath
from .endpoints import Endpoint
from .responses import LudicResponse, run_in_threadpool_safe
from .routing import Router

TCallable = TypeVar("TCallable", bound=Callable[..., Any])
TEndpoint = TypeVar("TEndpoint", bound=Endpoint[Attrs])


class LudicApp(Starlette):
    """Starlette application with Ludic adoption.

    Example:

        async def homepage(request: Request) -> html:
            return html(...)

        app = LudicApp(debug=True)
        app.add_route("/", homepage)

    You can also use a method decorator to register a Ludic endpoint:

        @app.get("/")
        async def homepage(request: Request) -> button:
            return button(...)
    """

    router: Router

    def __init__(
        self,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, TCallable] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[AppType] | None = None,
    ) -> None:
        super().__init__(debug, middleware=middleware)

        for key, value in (exception_handlers or {}).items():
            self.add_exception_handler(key, value)

        self.router = Router(
            routes, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )

    def get(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register GET endpoint to the application."""
        return self.register_route(path, method="GET", **kwargs)

    def head(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register GET endpoint to the application."""
        return self.register_route(path, method="HEAD", **kwargs)

    def post(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register POST endpoint to the application."""
        return self.register_route(path, method="POST", **kwargs)

    def put(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register PUT endpoint to the application."""
        return self.register_route(path, method="PUT", **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register DELETE endpoint to the application."""
        return self.register_route(path, method="DELETE", **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register PATCH endpoint to the application."""
        return self.register_route(path, method="PATCH", **kwargs)

    def options(self, path: str, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Register OPTIONS endpoint to the application."""
        return self.register_route(path, method="OPTIONS", **kwargs)

    def register_route(
        self,
        path: str,
        method: Literal[
            "GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"
        ] = "GET",
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> Callable[[TCallable], TCallable]:
        """Register an endpoint to the application."""

        def register(handler: TCallable) -> TCallable:
            self.add_route(
                path,
                handler,
                methods=[method],
                name=name,
                include_in_schema=include_in_schema,
            )
            return handler

        return register

    def endpoint(
        self,
        path: str,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> Callable[[type[TEndpoint]], type[TEndpoint]]:
        """Register a Ludic class endpoint to the application."""

        def register(endpoint: type[TEndpoint]) -> type[TEndpoint]:
            self.add_route(
                path, endpoint, name=name, include_in_schema=include_in_schema
            )
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
        """Add a Ludic endpoint to the application.

        The endpoint will be wrapped in a :class:`LudicResponse`
        if a Ludic component is returned. This means that it is possible to return
        a Ludic component instance from the handler directly instead of wrapping it
        in the :class:`LudicResponse`.

        It is still possible to return a regular response from the handler
        (e.g. ``JSONResponse({"hello": "world"})``).
        """
        super().add_route(
            path,
            route,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )

    def url_path_for(self, name: str, /, **path_params: Any) -> URLPath:
        """Get the URL path for an endpoint.

        Args:
            name: The name of the endpoint.
            **path_params: The path parameters.

        Returns:
            The URL path.
        """
        return self.router.url_path_for(name, **path_params)

    def add_exception_handler(
        self,
        exc_class_or_status_code: int | type[Exception],
        handler: TCallable,
    ) -> None:
        """Add an exception handler to the application.

        Example:

            async def not_found(request: Request, exc: HTTPException):
                return Page(
                    Header("Page Could Not Be Found"),
                    Body(f"Here is the reason: {exc.detail}")
                )

            app.add_exception_handler(404, not_found)

        Args:
            exc_class_or_status_code: The exception class or status code.
            handler: The exception handler function.
        """

        @wraps(handler)
        async def wrapped_handler(
            request: Request | WebSocket, exc: Exception
        ) -> Response:
            parameters = inspect.signature(handler).parameters
            handler_kw: dict[str, Any] = {}
            is_async = is_async_callable(handler)

            for name, param in parameters.items():
                if issubclass(param.annotation, Exception):
                    handler_kw[name] = exc
                elif issubclass(param.annotation, Request):
                    handler_kw[name] = request

            if is_async:
                with BaseElement.formatter:
                    response = await handler(**handler_kw)
            else:
                response = await run_in_threadpool_safe(handler, **handler_kw)

            if isinstance(response, BaseElement):
                return LudicResponse(response, getattr(exc, "status_code", 500))
            return cast(Response, response)

        self.exception_handlers[exc_class_or_status_code] = wrapped_handler

    def exception_handler(
        self, exc_class_or_status_code: int | type[Exception]
    ) -> Callable[[TCallable], TCallable]:
        """Register an exception handler to the application.

        Example:

            @app.exception_handler(404)
            async def not_found(request: Request, exc: HTTPException):
                return Page(
                    Header("Page Could Not Be Found"),
                    Body(f"Here is the reason: {exc.detail}")
                )
        """

        def decorator(handler: TCallable) -> TCallable:
            self.add_exception_handler(exc_class_or_status_code, handler)
            return handler

        return decorator
