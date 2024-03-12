import json
from collections.abc import MutableMapping
from typing import Any
from urllib.parse import urlencode

from starlette.datastructures import (
    FormData,
    QueryParams,
)
from starlette.datastructures import Headers as BaseHeaders
from starlette.datastructures import (
    URLPath as BaseURLPath,
)

from ludic import types

__all__ = ("FormData", "Headers", "QueryParams", "URLPath")


class Headers(BaseHeaders):
    """An immutable, case-insensitive multi-dict representing HTTP headers."""

    def __init__(
        self,
        headers: types.Headers | None = None,
        raw: list[tuple[bytes, bytes]] | None = None,
        scope: MutableMapping[str, Any] | None = None,
    ) -> None:
        new_headers: dict[str, str] = {}

        if headers:
            for key, value in headers.items():
                if isinstance(value, str):
                    new_headers[key] = value
                else:
                    new_headers[key] = json.dumps(value)

        super().__init__(new_headers, raw, scope)


class URLPath(BaseURLPath):
    """A URL path string that may also hold an associated protocol and/or host.

    Used by the routing to return `url_path_for` matches.
    """

    def query(self, **kwargs: Any) -> "URLPath":
        query = urlencode([(str(key), str(value)) for key, value in kwargs.items()])
        return URLPath(f"{self}?{query}", self.protocol, self.host)
