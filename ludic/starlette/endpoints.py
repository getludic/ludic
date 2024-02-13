from collections.abc import Callable
from typing import Any, ClassVar

from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.requests import Request
from starlette.routing import Route
from typing_extensions import TypeVar

from ..attrs import BaseAttrs
from ..base import Component, Element
from .response import LudicResponse

_Ta = TypeVar("_Ta", bound=BaseAttrs, default=BaseAttrs)


class HTTPEndpoint(BaseEndpoint):  # type: ignore
    """Endpoint class for PyMX components.

    Usage:

        class MyButtonEndpoint(PyMXEndpoint):
            async def get(self, request: Request) -> button:
                return button(...)
    """

    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        handler_name = (
            "get"
            if request.method == "HEAD" and not hasattr(self, "head")
            else request.method.lower()
        )

        handler: Callable[[Request], Any] = getattr(
            self, handler_name, self.method_not_allowed
        )
        is_async = is_async_callable(handler)
        if is_async:
            response = await handler(request)
        else:
            response = await run_in_threadpool(handler, request)
        if isinstance(response, Element):
            response = LudicResponse(response)
        await response(self.scope, self.receive, self.send)


class Endpoint(Component[_Ta]):
    """Base class for PyMX endpoints."""

    route: ClassVar[Route]

    def url_for(self, endpoint: type["Endpoint"], **kwargs: Any) -> str:
        url_kwargs: dict[str, Any] = {}
        for param_name in endpoint.route.param_convertors.keys():
            if param_name in kwargs:
                url_kwargs[param_name] = kwargs[param_name]
            if param_name in self.attrs:
                url_kwargs[param_name] = self.attrs[param_name]
        return endpoint.route.url_path_for(endpoint.__name__, **url_kwargs)
