import itertools
from collections.abc import Callable
from typing import Any

import starlette
from starlette.datastructures import URL, URLPath
from starlette.routing import NoMatchFound, Route, Router


def join_mounts(prefix: str, suffix: str) -> str:
    """Join mount prefixes and suffixes.

    Args:
        prefix: The prefix to join.
        suffix: The suffix to join.
    """
    prefixes = prefix.split(":")
    suffixes = suffix.split(":")

    for part in prefixes:
        if suffixes and suffixes[0] == part:
            suffixes.pop(0)

    return ":".join(itertools.chain(prefixes, suffixes))


class Request(starlette.requests.Request):
    def url_path_for(
        self, endpoint: str | Callable[..., Any], /, **path_params: Any
    ) -> URLPath:
        """Get URL path for an endpoint.

        Args:
            endpoint: The endpoint to get the URL path for, can be name or a registered
                endpoint class.
            **path_params: URL path parameters.

        Returns:
            The URL path.
        """
        router: Router = self.scope["router"]

        if isinstance(endpoint, str):
            endpoint_name = endpoint
        elif (route := getattr(endpoint, "route", None)) and isinstance(route, Route):
            endpoint_name = route.name
        else:
            raise NoMatchFound(str(endpoint), path_params)

        try:
            return router.url_path_for(endpoint_name, **path_params)
        except NoMatchFound as e:
            if partial_mount := self.scope.get("partial_mount"):
                return router.url_path_for(
                    join_mounts(partial_mount, endpoint_name),
                    **path_params,
                )
            else:
                raise e

    def url_for(self, endpoint: str | Callable[..., Any], /, **path_params: Any) -> URL:
        """Get URL for an endpoint.

        Args:
            endpoint: The endpoint to get the URL for, can be name or a registered
                endpoint class.
            **path_params: URL path parameters.

        Returns:
            The URL.
        """
        url_path = self.url_path_for(endpoint, **path_params)
        return url_path.make_absolute_url(base_url=self.base_url)
