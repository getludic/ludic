from typing import Any
from urllib.parse import urlencode

from starlette.datastructures import (
    FormData,
    Headers,
    QueryParams,
)
from starlette.datastructures import (
    URLPath as BaseURLPath,
)

__all__ = ("FormData", "Headers", "QueryParams", "URLPath")


class URLPath(BaseURLPath):
    """A URL path string that may also hold an associated protocol and/or host.

    Used by the routing to return `url_path_for` matches.
    """

    def query(self, **kwargs: Any) -> "URLPath":
        query = urlencode([(str(key), str(value)) for key, value in kwargs.items()])
        return URLPath(f"{self}?{query}", self.protocol, self.host)
