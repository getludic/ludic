import inspect
from collections.abc import Callable
from typing import Any

from starlette._utils import is_async_callable
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.types import Receive, Scope, Send

from ..elements.base import Element
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
    """

    def add_pymx_route(
        self, path: str, handler: Callable[..., Any], **kwargs: Any
    ) -> None:
        """Add a PyMX endpoint to the application.

        The endpoint will be wrapped in a :class:`~pymx.starlette.response.PyMXResponse`
        so that it is possible to return a component instance from the handler.
        """
        if inspect.isfunction(handler) or inspect.ismethod(handler):
            handler = _PyMXHandler(handler)
        super().add_route(path, handler, **kwargs)
