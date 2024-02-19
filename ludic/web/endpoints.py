from collections.abc import Callable
from typing import Any, ClassVar, Never, Protocol

from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.requests import Request
from starlette.routing import Route

from ludic.types import Component, Element, TAttr
from ludic.utils import get_element_generic_args

from .response import LudicResponse
from .utils import extract_from_request


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


class HTTPEndpoint(BaseEndpoint):
    """Endpoint class for Ludic components.

    Usage:

        class MyButtonEndpoint(HTTPEndpoint):
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

        handler: Callable[[Request], Any] = (
            getattr(self, handler_name, None) or self.method_not_allowed
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


class Endpoint(Component[Never, TAttr]):
    """Base class for Ludic endpoints."""

    route: ClassVar[Route]

    def url_for(self, endpoint: type[RoutedProtocol], **kwargs: Any) -> str:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint.
            **kwargs: URL path parameters.

        Returns:
            The URL.
        """
        endpoint_generic_args = get_element_generic_args(endpoint)
        self_generic_args = get_element_generic_args(self)

        if (
            endpoint_generic_args
            and self_generic_args
            and endpoint_generic_args[-1] is self_generic_args[-1]
        ):
            kwargs = {**self.attrs, **kwargs}

        return url_for(endpoint, **kwargs)
