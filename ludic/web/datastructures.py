import json
from collections.abc import MutableMapping
from typing import Any

from starlette.datastructures import (
    URL,
    FormData,
    QueryParams,
    URLPath,
)
from starlette.datastructures import Headers as BaseHeaders

from ludic import types

__all__ = ("FormData", "Headers", "QueryParams", "URL", "URLPath")


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
