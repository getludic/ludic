import inspect
from collections.abc import Callable
from typing import Any, ClassVar, Protocol

from starlette.datastructures import URL
from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.routing import Route

from ludic.catalog.loaders import LazyLoader
from ludic.components import Component
from ludic.types import AnyChildren, NoChildren, TAttrs
from ludic.utils import get_element_generic_args

from .requests import Request
from .responses import prepare_response


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
        response = await prepare_response(handler, request)

        await response(self.scope, self.receive, self.send)


class Endpoint(Component[NoChildren, TAttrs]):
    """Base class for Ludic endpoints."""

    route: ClassVar[Route]

    @property
    def request(self) -> Request | None:
        """The current request."""
        return self.context.get("request")

    def lazy_load(
        self,
        endpoint: type[RoutedProtocol],
        placeholder: AnyChildren = "Loading ...",
        **kwargs: Any,
    ) -> LazyLoader:
        """Lazy load an endpoint's content.

        Args:
            endpoint (type[RoutedProtocol]): The endpoint to lazy load.
            placeholder (AnyChild): The content to show while loading.
            **kwargs: URL path parameters.
        """
        return LazyLoader(
            placeholder=placeholder,
            load_url=self.url_for(endpoint, **kwargs).path,
        )

    def url_for(self, endpoint: type[RoutedProtocol] | str, **path_params: Any) -> URL:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint.
            **path_params: URL path parameters.

        Returns:
            The URL.
        """
        if self.request is None or not isinstance(self.request, Request):
            raise RuntimeError(
                f"{type(self).__name__} is not bound to a request, you can only use "
                f"the {type(self).__name__}.url_for method in the context of a request."
            )

        if inspect.isclass(endpoint) and issubclass(endpoint, Endpoint):
            endpoint_generic_args = get_element_generic_args(endpoint)
            self_generic_args = get_element_generic_args(type(self))

            if (
                endpoint_generic_args
                and self_generic_args
                and endpoint_generic_args[-1] is self_generic_args[-1]
            ):
                path_params = {
                    key: value
                    for key, value in {**self.attrs, **path_params}.items()
                    if key in endpoint.route.param_convertors
                }

        return self.request.url_for(endpoint, **path_params)
