from collections.abc import Callable
from typing import Any, ClassVar, Protocol

from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.requests import Request
from starlette.routing import Route
from typing_extensions import TypeVar

from ludic.attrs import BaseAttrs
from ludic.base import Component, Element

from .response import LudicResponse
from .utils import extract_from_request

Ta = TypeVar("Ta", bound=BaseAttrs, default=BaseAttrs)


class RoutedProtocol(Protocol):
    route: ClassVar[Route]


def url_for(endpoint: type[RoutedProtocol], **kwargs: Any) -> str:
    """Get URL for an endpoint.

    Args:
        endpoint: The endpoint.
        **kwargs: URL path parameters.

    Returns:
        The URL.
    """
    url_kwargs: dict[str, Any] = {}
    for param_name in endpoint.route.param_convertors.keys():
        if param_name in kwargs:
            url_kwargs[param_name] = kwargs[param_name]
    return endpoint.route.url_path_for(endpoint.__name__, **url_kwargs)


class HTTPEndpoint(BaseEndpoint):  # type: ignore
    """Endpoint class for PyMX components.

    Usage:

        class MyButtonEndpoint(PyMXEndpoint):
            async def get(self, request: Request) -> button:
                return button(...)
    """

    route: ClassVar[Route]

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
        handler_kw = await extract_from_request(handler, request)

        is_async = is_async_callable(handler)
        if is_async:
            response = await handler(request, **handler_kw)
        else:
            response = await run_in_threadpool(handler, request, **handler_kw)

        if isinstance(response, Element):
            response = LudicResponse(response)

        await response(self.scope, self.receive, self.send)


class Endpoint(Component[Ta]):
    """Base class for PyMX endpoints."""

    route: ClassVar[Route]

    def url_for(self, endpoint: type[RoutedProtocol], **kwargs: Any) -> str:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint.
            **kwargs: URL path parameters.

        Returns:
            The URL.
        """
        return url_for(endpoint, **{**self.attrs, **kwargs})
