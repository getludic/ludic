from collections.abc import Callable
from typing import Any

from starlette.datastructures import URL, URLPath
from starlette.requests import Request as StarletteRequest
from starlette.routing import Route, Router, get_name


class Request(StarletteRequest):
    def url_for(self, endpoint: str | Callable[..., Any], /, **path_params: Any) -> URL:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint to get the URL for, can be name or a registered
                endpoint class.
            **path_params: URL path parameters.

        Returns:
            The URL.
        """
        url_path: URLPath
        if (
            not isinstance(endpoint, str)
            and (route := getattr(endpoint, "route", None))
            and isinstance(route, Route)
        ):
            url_path = route.url_path_for(route.name, **path_params)
        else:
            router: Router = self.scope["router"]
            if not isinstance(endpoint, str):
                endpoint = get_name(endpoint)
            url_path = router.url_path_for(endpoint, **path_params)
        return url_path.make_absolute_url(base_url=self.base_url)
