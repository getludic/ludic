import inspect
from collections.abc import Callable
from typing import Any, ClassVar, Protocol

from starlette._utils import is_async_callable
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.requests import Request
from starlette.routing import Route

from ludic.html import div
from ludic.types import AnyChild, BaseElement, Component, NoChild, TAttrs
from ludic.utils import get_element_generic_args

from .responses import LudicResponse
from .utils import extract_from_request


class RoutedProtocol(Protocol):
    route: ClassVar[Route]


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

        handler: Callable[..., Any] = (
            getattr(self, handler_name, None) or self.method_not_allowed
        )
        handler_kw = await extract_from_request(handler, request)

        is_async = is_async_callable(handler)
        if is_async:
            response = await handler(**handler_kw)
        else:
            response = await run_in_threadpool(handler, **handler_kw)

        if isinstance(response, BaseElement):
            response = LudicResponse(response)

        await response(self.scope, self.receive, self.send)


class Endpoint(Component[NoChild, TAttrs]):
    """Base class for Ludic endpoints."""

    route: ClassVar[Route]
    app: ClassVar[Starlette]

    def lazy_load(
        self,
        endpoint: type[RoutedProtocol],
        placeholder: AnyChild = "Loading ...",
        **kwargs: Any,
    ) -> div:
        """Lazy load an endpoint's content.

        Args:
            endpoint (type[RoutedProtocol]): The endpoint to lazy load.
            placeholder (AnyChild): The content to show while loading.
            **kwargs: URL path parameters.
        """
        return div(
            placeholder,
            hx_get=self.url_for(endpoint, **kwargs),
            hx_trigger="load",
        )

    def url_for(self, endpoint: type[RoutedProtocol] | str, **kwargs: Any) -> str:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint.
            **kwargs: URL path parameters.

        Returns:
            The URL.
        """
        if not hasattr(self, "app"):
            raise RuntimeError(
                f"{type(self).__name__} is not bound to an app, you need to set the"
                f"{type(self).__name__}.app property in order to use Endpoint.url_for."
            )

        if inspect.isclass(endpoint) and issubclass(endpoint, Endpoint):
            endpoint_generic_args = get_element_generic_args(endpoint)
            self_generic_args = get_element_generic_args(self)

            if (
                endpoint_generic_args
                and self_generic_args
                and endpoint_generic_args[-1] is self_generic_args[-1]
            ):
                kwargs = {
                    key: value
                    for key, value in {**self.attrs, **kwargs}.items()
                    if key in endpoint.route.param_convertors
                }

        endpoint_name = endpoint if isinstance(endpoint, str) else endpoint.route.name
        return str(self.app.url_path_for(endpoint_name, **kwargs))
