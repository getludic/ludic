from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal

from starlette.applications import AppType, Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
from starlette.types import ExceptionHandler, Lifespan

from .endpoints import Endpoint
from .routing import LudicRouter


class LudicApp(Starlette):
    """Starlette application with Ludic methods.

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

    def __init__(
        self,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[AppType] | None = None,
    ) -> None:
        exception_handlers = exception_handlers or {}
        super().__init__(
            debug, middleware=middleware, exception_handlers=exception_handlers
        )
        self.router = LudicRouter(
            routes, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )

    def get(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register GET endpoint to the application."""
        return self.register_route(path, method="GET", **kwargs)

    def post(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register POST endpoint to the application."""
        return self.register_route(path, method="POST", **kwargs)

    def put(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register PUT endpoint to the application."""
        return self.register_route(path, method="PUT", **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register DELETE endpoint to the application."""
        return self.register_route(path, method="DELETE", **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Callable[..., Any]:
        """Register PATCH endpoint to the application."""
        return self.register_route(path, method="PATCH", **kwargs)

    def register_route(
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
        """Register a Ludic class endpoint to the application."""

        def register(endpoint: type[Endpoint]) -> type[Endpoint]:
            self.add_route(path, endpoint, include_in_schema=include_in_schema)
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
