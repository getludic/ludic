import inspect
from collections.abc import Callable
from typing import Any, ClassVar, Protocol

from starlette.endpoints import HTTPEndpoint as BaseEndpoint
from starlette.requests import Request
from starlette.routing import Route

from ludic.catalog.loading import LazyLoader
from ludic.types import AnyChildren, Component, NoChildren, TAttrs
from ludic.utils import get_element_generic_args

from .datastructures import URLPath
from .responses import prepare_response


class AppProtocol(Protocol):
    def url_path_for(self, name: str, /, **path_params: Any) -> URLPath: ...


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
    app: ClassVar[AppProtocol]

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
            load_url=self.url_for(endpoint, **kwargs),
        )

    def url_for(
        self, endpoint: type[RoutedProtocol] | str, **path_params: Any
    ) -> URLPath:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint.
            **path_params: URL path parameters.

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
                path_params = {
                    key: value
                    for key, value in {**self.attrs, **path_params}.items()
                    if key in endpoint.route.param_convertors
                }

        endpoint_name = endpoint if isinstance(endpoint, str) else endpoint.route.name
        return self.app.url_path_for(endpoint_name, **path_params)
